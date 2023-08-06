# Copyright 2022 Inductor, Inc.

"""Defines and implements a table catalog."""

import importlib
import json
import sqlite3
from typing import Any, Callable, Dict, List, Optional, Tuple

import boto3
import psycopg2
from psycopg2 import extras
import pymysql

from inductor import environment
from inductor import util
from inductor.data.table import dynamodb
from inductor.data.table import mysql
from inductor.data.table import postgresql
from inductor.data.table import sqlite
from inductor.data.table import table
from inductor.data.table import table_util


class TableCatalog:
    """A Table catalog."""

    def __init__(
        self,
        metadata_table: table.WithPrimaryKey,
        name_to_id_table: table.WithPrimaryKey,
        env: environment.Env,
        run_time: bool,
        database_url: str,
        unique_id: Callable[[], str],
        secrets: Optional[Dict[str, Any]] = None,
        physical_table_name_prefix: Optional[str] = None):
        """Constructs a new TableCatalog.

        Args:
            metadata_table: Table used to persist the metadata of the catalogued
                tables. Keyed by table ID.
            name_to_id_table: Table used to persist the mapping from table names
                to table IDs.
            env: Environment in which this catalog is to be used.
            run_time: If True, then this catalog is being used at run time.
            database_url: URL identifying database in which to store tables
                created by this catalog.  Must be in one of the formats
                accepted by table_util.table_from_url().
            unique_id: Function that returns a unique ID.
            secrets: Optionally, a dictionary of secrets to be used by tables
                created by this catalog.
            physical_table_name_prefix: Optionally, prefix to be used when
                naming tables in underlying data systems.
        """
        self._metadata_table = metadata_table
        self._name_to_id_table = name_to_id_table
        self._env = env
        self._run_time = run_time
        self._database_url = database_url
        self._unique_id = unique_id
        self._secrets = {} if secrets is None else secrets
        self._table_creation_instructions: List[
            Tuple[str, Dict[str, Any]]] = []
        self._physical_table_name_prefix = physical_table_name_prefix

    def __getitem__(self, table_name: str) -> table.Table:
        """Returns Table having given table_name in this catalog.

        Args:
            table_name: Name of a table in this catalog.

        Raises:
            KeyError if no table having given table_name exists in this
            TableCatalog.
        """
        # Get table ID from name_to_id table
        table_id = self._name_to_id_table[table_name]["id"]
        # Retrieve relevant information from metadata table
        row = self._metadata_table[table_id]
        module_qualname = row["table_module_qualname"]
        class_qualname = row["table_class_qualname"]
        metadata = json.loads(row["table_json"])
        existing_table = row["existing_table"]
        # Retrieve secrets from metadata table, secrets file, or
        # self._database_url
        if existing_table:
            secrets = self._secrets.get(table_name)
        elif class_qualname.startswith("Sqlite"):
            secrets = {}
        else:
            system, username, password, host, _, database = (
                table_util.parse_database_url(self._database_url))
            if (class_qualname.lower().startswith(system) and
                username == metadata["user"] and
                host == metadata["host"] and
                database == metadata["database"]):
                secrets = {"password": password}
        if not secrets:
            secrets = json.loads(row.get("table_secrets") or "{}")
        metadata = {**metadata, **secrets}
        # Obtain relevant table subclass
        table_subclass = importlib.import_module(module_qualname)
        for name in class_qualname.split("."):
            table_subclass = getattr(table_subclass, name)
        # Instantiate and return Table
        return table_subclass.from_metadata(metadata)

    def _up(self):
        """Executes any pre-run-time table creation or addition instructions."""
        # TODO: Remove need to "trick" the table creation functions
        # by setting self._run_time to True here.
        self._run_time = True
        for method_name, table_spec in self._table_creation_instructions:
            getattr(self, method_name)(**table_spec)
        self._run_time = False

    def table_spec(self, table_name: str) -> Dict[str, Any]:
        """Returns table_spec for table having given table_name.

        Args:
            table_name: Name of a table in this catalog.

        Raises:
            KeyError if no table having given table_name exists in this
            TableCatalog.
        """
        table_id = self._name_to_id_table[table_name]["id"]
        return json.loads(self._metadata_table[table_id]["table_spec"])

    def __contains__(self, table_name: str) -> bool:
        """Returns True if and only if table_name is present in this catalog.

        Args:
            table_name: Table name for which to determine presence.
        """
        return table_name in self._name_to_id_table

    def _add_table(
        self,
        table_name: str,
        t: table.Table,
        table_spec: Dict[str, Any],
        skip_if_exists: bool,
        existing_table: bool,
        table_secrets: Optional[Dict[str, Any]] = None) -> bool:
        """Adds references to given table t to this TableCatalog.

        If a table having given table_name already exists in this
        TableCatalog and skip_if_exists is False, then the references to it are
        replaced (the previous table is not deleted from its underlying
        storage system).

        Args:
            table_name: Name under which table is to be added to this
                TableCatalog.
            t: Table to be added to this TableCatalog.
            table_spec: Specification of this table's characteristics.
                Must be JSON-serializable.
            skip_if_exists: If True, then this method does nothing if a table
                having given table_name already exists in this catalog.
            existing_table: If True, then this table already exists in its
                underlying storage system.
            table_secrets: Optionally, secrets for this table. Must be
                JSON-serializable.

        Returns:
            True if table references were added or replaced,
                and False otherwise.
        """
        if skip_if_exists and table_name in self:
            return False

        table_id = self._unique_id()

        # Since table_id is a newly generated unique id,
        # it will never already exist in self._metadata_table.
        assert self._metadata_table.set(
            table_id,
            {
                "table_module_qualname": util.module_qualname(t.__class__),
                "table_class_qualname": t.__class__.__qualname__,
                "table_json": json.dumps(
                    t.to_metadata(), separators=(",", ":")),
                "table_spec": json.dumps(table_spec, separators=(",", ":")),
                "existing_table": existing_table,
                "table_secrets": None if table_secrets is None else
                    json.dumps(table_secrets, separators=(",", ":"))
            },
            skip_if_exists=True
        )

        return self._name_to_id_table.set(
            table_name,
            {
                "id": table_id
            },
            skip_if_exists=skip_if_exists
        )

    def create_table(
        self,
        name: str,
        *,  # all subsequent parameters are keyword-only
        faster_query_columns: Optional[List[str]] = None):
        """Creates (as necessary) a table having the given name.

        The table will be appendable and SQL-SELECT-queryable.  If a table
        having the given name already exists in this app, then it must have the
        characteristics specified by this method call's arguments, in which case
        no new table is created (i.e., in that case, this method is idempotent);
        otherwise, this method raises an exception.

        Args:
            name: Name for this table.
            faster_query_columns: Names of columns for which SQL SELECT queries
                should be accelerated (generally via creation of indexes).

        Raises:
            RuntimeError if a table having given name already exists but does
            not have the characteristics specified by this method call's
            arguments.
        """
        table_spec = locals().copy()
        del table_spec["self"]
        if not self._run_time:
            self._table_creation_instructions.append(
                (self.create_table.__name__, table_spec))
        elif isinstance(self._env, (environment.Local, environment.Server)):
            if name in self:
                if self.table_spec(name) != table_spec:
                    raise RuntimeError(
                        f"Table {name} already exists but has different "
                        "table_spec.")
            else:
                if self._physical_table_name_prefix is None:
                    physical_table_name = f"{self._unique_id()}"
                else:
                    physical_table_name = (
                        f"{self._physical_table_name_prefix}"
                        f"_{self._unique_id()}")
                t = table_util.table_from_url(
                    database_url=self._database_url,
                    table_name=physical_table_name,
                    primary_key_column=None,
                    indexed_columns=(
                        set(faster_query_columns) if faster_query_columns
                        else set()))
                already_exists = not self._add_table(
                    name, t, table_spec, skip_if_exists=True,
                    existing_table=False)
                if (already_exists and
                    self.table_spec(name) != table_spec):
                    raise RuntimeError(
                        f"Table {name} already exists but has different "
                        "table_spec.")
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")

    def create_keyed_table(
        self,
        name: str,
        key_column: str,
        *,
        sql_queryable: bool = True,  # pylint: disable=unused-argument
        range_queries_only: bool = False,  # pylint: disable=unused-argument
        faster_query_columns: Optional[List[str]] = None):
        """Creates (as necessary) a keyed table having the given name.

        The table will be writable.  If a table having the given name already
        exists in this app, then it must have the characteristics specified by
        this method call's arguments, in which case no new table is created
        (i.e., in that case, this method is idempotent); otherwise, this method
        raises an exception.

        Args:
            name: Name for this table.
            key_column: Name of the column containing each row's unique key
                value.
            sql_queryable: Should the table natively support SQL SELECT queries?
            range_queries_only: If sql_queryable is True, should the table
                only natively support range queries?  Ignored if sql_queryable
                is False.
            faster_query_columns: Names of columns for which SQL SELECT queries
                should be accelerated (generally via creation of indexes).

        Raises:
            RuntimeError if a table having given name already exists but does
            not have the characteristics specified by this method call's
            arguments.
        """
        table_spec = locals().copy()
        del table_spec["self"]
        if not self._run_time:
            self._table_creation_instructions.append(
                (self.create_keyed_table.__name__, table_spec))
        elif isinstance(self._env, (environment.Local, environment.Server)):
            if name in self:
                if self.table_spec(name) != table_spec:
                    raise RuntimeError(
                        f"Table {name} already exists but has different "
                        "table_spec.")
            else:
                if self._physical_table_name_prefix is None:
                    physical_table_name = f"{self._unique_id()}"
                else:
                    physical_table_name = (
                        f"{self._physical_table_name_prefix}"
                        f"_{self._unique_id()}")
                t = table_util.table_from_url(
                    database_url=self._database_url,
                    table_name=physical_table_name,
                    primary_key_column=key_column,
                    indexed_columns=(
                        set(faster_query_columns) if faster_query_columns
                        else set()))
                already_exists = not self._add_table(
                    name, t, table_spec, skip_if_exists=True,
                    existing_table=False)
                if (already_exists and
                    self.table_spec(name) != table_spec):
                    raise RuntimeError(
                        f"Table {name} already exists but has different "
                        "table_spec.")
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")

    def add_existing_sqlite_table(
        self,
        name: str,
        sqlite_file_path: str,
        sqlite_table_name: Optional[str] = None,
        primary_key_column: Optional[str] = None):
        """Adds a reference in this app to an existing sqlite table.

        If a table is already referenced in this app under the given name, then
        it must have the characteristics specified by this method call's
        arguments; otherwise, this method raises an exception.

        Args:
            name: Name in this app under which to add a reference to the
                specified existing sqlite table.
            sqlite_file_path: Path to file giving sqlite database containing
                the existing table to be added.
            sqlite_table_name: Name of existing table in file given by
                sqlite_file_path. If not provided, the value of the name
                argument is used.
            primary_key_column: If non-None, then the table will be treated as
                being keyed by the column having name given by this parameter.
                If None:
                - If the existing table has exactly one primary key column, then
                  the table will be treated as being keyed on that column.
                - Otherwise, if the existing table has no primary key column
                  and exactly one unique index column, then the table will be
                  treated as being keyed on that column.
                - Otherwise, the table will not be treated as being keyed.

        Raises:
            RuntimeError if a table having given name already exists but does
            not have the characteristics specified by this method call's
            arguments.
        """
        if sqlite_table_name is None:
            sqlite_table_name = name
        table_spec = locals().copy()
        del table_spec["self"]
        if not self._run_time:
            self._table_creation_instructions.append(
                (self.add_existing_sqlite_table.__name__, table_spec))
        elif name in self:
            if self.table_spec(name) != table_spec:
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")
        else:
            if not primary_key_column:
                conn = sqlite3.connect(sqlite_file_path)
                conn.row_factory = sqlite3.Row
                table_columns_info = list(conn.execute(
                    f"PRAGMA table_info({sqlite_table_name})"))
                pk_columns_info = [
                    r for r in table_columns_info if r["pk"] > 0]
                if len(pk_columns_info) == 1:
                    primary_key_column = pk_columns_info[0]["name"]
                elif len(pk_columns_info) == 0:
                    table_indexes = list(conn.execute(
                        f"PRAGMA index_list({sqlite_table_name})"))
                    unique_indexes = [
                        r for r in table_indexes if r["unique"] == 1]
                    if len(unique_indexes) == 1:
                        index_name = unique_indexes[0]["name"]
                        unique_index_columns_info = list(conn.execute(
                            f"PRAGMA index_info({index_name})"))
                        if len(unique_index_columns_info) == 1:
                            primary_key_column = unique_index_columns_info[0][
                                "name"]
                conn.close()
            if primary_key_column:
                t = sqlite.SqliteKeyedTable(
                    sqlite_file_path, sqlite_table_name, primary_key_column,
                    auto_ddl=False)
            else:
                t = sqlite.SqliteTable(
                    sqlite_file_path, sqlite_table_name, auto_ddl=False)
            already_exists = not self._add_table(
                name, t, table_spec, skip_if_exists=True, existing_table=True)
            if (already_exists and
                self.table_spec(name) != table_spec):
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")

    def add_existing_mysql_table(
        self,
        name: str,
        mysql_host: str,
        mysql_user: str,
        mysql_database: str,
        mysql_table_name: Optional[str] = None,
        primary_key_column: Optional[str] = None,
        mysql_port: Optional[int] = None,
        mysql_password: Optional[str] = None):
        """Adds a reference in this app to an existing MySQL table.

        If a table is already referenced in this app under the given name, then
        it must have the characteristics specified by this method call's
        arguments; otherwise, this method raises an exception.

        Args:
            name: Name in this app under which to add a reference to the
                specified existing MySQL table.
            mysql_host: Host name of database server hosting the MySQL database
                containing the existing table to be added.
            mysql_user: MySQL database server username.
            mysql_database: Name of MySQL database containing existing table.
            mysql_table_name: Name of existing table in database given by
                preceding arguments. If not provided, the value of the name
                argument is used.
            primary_key_column: If non-None, then the table will be treated as
                being keyed by the column having name given by this parameter.
                If None:
                - If the existing table has exactly one primary key column, then
                  the table will be treated as being keyed on that column.
                - Otherwise, if the existing table has no primary key column
                  and exactly one unique index column, then the table will be
                  treated as being keyed on that column.
                - Otherwise, the table will not be treated as being keyed.
            mysql_port: Optionally, the port on which to connect to the database
                server.
            mysql_password: Optionally, password for user.  If not provided,
                password must be provided by secrets file.

        Raises:
            RuntimeError if a table having given name already exists but does
            not have the characteristics specified by this method call's
            arguments.
        """
        if mysql_table_name is None:
            mysql_table_name = name

        table_spec = locals().copy()
        del table_spec["self"]
        if not self._run_time:
            self._table_creation_instructions.append(
                (self.add_existing_mysql_table.__name__, table_spec))
            return

        del table_spec["mysql_password"]
        password = (mysql_password if mysql_password is not None
                    else self._secrets.get(name, {}).get("mysql_password"))
        if password is None:
            raise ValueError("No mysql_password was provided for "
                             f"table {name}.")

        if name in self:
            if self.table_spec(name) != table_spec:
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")
        else:
            if not primary_key_column:
                conn_params = {
                    "host": mysql_host,
                    "user": mysql_user,
                    "password": password,
                    "database": mysql_database,
                    "cursorclass": pymysql.cursors.DictCursor
                }
                if mysql_port:
                    conn_params["port"] = mysql_port
                conn = pymysql.connect(**conn_params)
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"SHOW KEYS FROM {mysql_table_name} "
                        "WHERE Key_name = 'PRIMARY'")
                    pk_columns = [
                        row["Column_name"] for row in cursor.fetchall()]
                if len(pk_columns) == 1:
                    primary_key_column = pk_columns[0]
                elif len(pk_columns) == 0:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            f"SHOW INDEX FROM {mysql_table_name} "
                            "WHERE Non_unique = 0")
                        unique_index_columns = [
                            row["Column_name"] for row in cursor.fetchall()]
                    if len(unique_index_columns) == 1:
                        primary_key_column = unique_index_columns[0]
                conn.close()
            table_args = {
                "host": mysql_host,
                "user": mysql_user,
                "password": mysql_password,
                "database": mysql_database,
                "table_name": mysql_table_name,
                "port": mysql_port,
                "auto_ddl": False,
            }
            if primary_key_column:
                table_args["primary_key_column"] = primary_key_column
                t = mysql.MysqlKeyedTable(**table_args)
            else:
                t = mysql.MysqlTable(**table_args)
            secrets = None if mysql_password is None else {
                "mysql_password": mysql_password
            }
            already_exists = not self._add_table(
                name, t, table_spec, table_secrets=secrets, skip_if_exists=True,
                existing_table=True)
            if already_exists and self.table_spec(name) != table_spec:
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")

    def add_existing_dynamodb_table(
        self,
        name: str,
        dynamodb_table_name: Optional[str] = None,
        dynamodb_endpoint_url: Optional[str] = None):
        """Adds a reference in this app to an existing DynamoDB table.

        If a table is already referenced in this app under the given name, then
        it must have the characteristics specified by this method call's
        arguments; otherwise, this method raises an exception.

        Args:
            name: Name in this app under which to add a reference to the
                specified existing DynamoDB table.
            dynamodb_table_name: Name of existing DynamoDB table. If not
                provided, the value of the name argument is used.
            dynamodb_endpoint_url: Optional Endpoint URL to be used to
                communicate with the DynamoDB service. Intended to be used
                to connect with a local DynamoDB instance for development
                and testing purposes. In general, should not be provided
                if utilizing an actual AWS account.

        Raises:
            RuntimeError if a table having given name already exists but does
            not have the characteristics specified by this method call's
            arguments.
        """
        if dynamodb_table_name is None:
            dynamodb_table_name = name
        table_spec = locals().copy()
        del table_spec["self"]
        if not self._run_time:
            self._table_creation_instructions.append(
                (self.add_existing_dynamodb_table.__name__, table_spec))
        elif name in self:
            if self.table_spec(name) != table_spec:
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")
        else:
            partition_key_column = None
            sort_key_column = None
            dynamodb_client = boto3.client(
                "dynamodb", endpoint_url=dynamodb_endpoint_url)
            table_description = dynamodb_client.describe_table(
                TableName=dynamodb_table_name)["Table"]
            key_schema = table_description["KeySchema"]
            for key in key_schema:
                if key["KeyType"] == "HASH":
                    partition_key_column = key["AttributeName"]
                elif key["KeyType"] == "RANGE":
                    sort_key_column = key["AttributeName"]
            assert partition_key_column is not None
            table_args = {
                "table_name": dynamodb_table_name,
                "partition_key_column": partition_key_column,
                "sort_key_column": sort_key_column,
                "endpoint_url": dynamodb_endpoint_url,
            }
            t = dynamodb.DynamoDBTable(**table_args)
            already_exists = not self._add_table(
                name, t, table_spec, skip_if_exists=True, existing_table=True)
            if (already_exists and
                self.table_spec(name) != table_spec):
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")

    def add_existing_postgresql_table(
        self,
        name: str,
        postgresql_host: str,
        postgresql_user: str,
        postgresql_database: str,
        postgresql_table_name: Optional[str] = None,
        primary_key_column: Optional[str] = None,
        postgresql_port: Optional[int] = None,
        postgresql_password: Optional[str] = None):
        """Adds a reference in this app to an existing PostgreSQL table.

        If a table is already referenced in this app under the given name, then
        it must have the characteristics specified by this method call's
        arguments; otherwise, this method raises an exception.

        Args:
            name: Name in this app under which to add a reference to the
                specified existing PostgreSQL table.
            postgresql_host: Host name of database server hosting the
                PostgreSQL database containing the existing table to be added.
            postgresql_user: PostgreSQL database server username.
            postgresql_database: Name of PostgreSQL database containing
                existing table.
            postgresql_table_name: Name of existing table in database given by
                preceding arguments. If not provided, the value of the name
                argument is used.
            primary_key_column: If non-None, then the table will be treated as
                being keyed by the column having name given by this parameter.
                If None:
                - If the existing table has exactly one primary key column,
                  then the table will be treated as being keyed on that column.
                - Otherwise, if the existing table has no primary key column
                  and exactly one unique index column, then the table will be
                  treated as being keyed on that column.
                - Otherwise, the table will not be treated as being keyed.
            postgresql_port: Optionally, the port on which to connect to the
                database server.
            postgresql_password: Optionally, password for user.  If not
                provided, password must be provided by secrets file.

        Raises:
            RuntimeError if a table having given name already exists but does
            not have the characteristics specified by this method call's
            arguments.
        """
        if postgresql_table_name is None:
            postgresql_table_name = name

        table_spec = locals().copy()
        del table_spec["self"]
        if not self._run_time:
            self._table_creation_instructions.append(
                (self.add_existing_postgresql_table.__name__, table_spec))
            return

        del table_spec["postgresql_password"]
        password = (postgresql_password if postgresql_password is not None
                    else self._secrets.get(name, {}).get("postgresql_password"))
        if password is None:
            raise ValueError("No postgresql_password was provided for "
                             f"table {name}.")

        if name in self:
            if self.table_spec(name) != table_spec:
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")
        else:
            if not primary_key_column:
                conn_params = {
                    "host": postgresql_host,
                    "user": postgresql_user,
                    "password": password,
                    "database": postgresql_database,
                    "cursor_factory": extras.RealDictCursor
                }
                if postgresql_port:
                    conn_params["port"] = postgresql_port
                conn = psycopg2.connect(**conn_params)
                # Reference for retrieving primary key columns:
                # https://wiki.postgresql.org/wiki/Retrieve_primary_key_columns
                select_key_expression = f"""
                    SELECT a.attname, format_type(a.atttypid, a.atttypmod)
                        AS data_type
                    FROM pg_index i
                    JOIN pg_attribute a ON a.attrelid = i.indrelid
                        AND a.attnum = ANY(i.indkey)
                    WHERE i.indrelid = '"{postgresql_table_name}"'::regclass
                    """
                select_primary_key_expression = (
                    select_key_expression + "AND i.indisprimary;")
                select_unique_key_expression = (
                    select_key_expression + "AND i.indisunique;")
                with conn.cursor() as cursor:
                    cursor.execute(select_primary_key_expression)
                    if cursor.rowcount == 1:
                        primary_key_column = cursor.fetchone()["attname"]
                    else:
                        cursor.execute(select_unique_key_expression)
                        if cursor.rowcount == 1:
                            primary_key_column = cursor.fetchone()["attname"]
                conn.commit()
                conn.close()
            table_args = {
                "host": postgresql_host,
                "user": postgresql_user,
                "password": password,
                "database": postgresql_database,
                "table_name": postgresql_table_name,
                "port": postgresql_port,
                "auto_ddl": False,
            }
            if primary_key_column:
                table_args["primary_key_column"] = primary_key_column
                t = postgresql.PostgresqlKeyedTable(**table_args)
            else:
                t = postgresql.PostgresqlTable(**table_args)
            secrets = None if postgresql_password is None else {
                "postgresql_password": postgresql_password
            }
            already_exists = not self._add_table(
                name, t, table_spec, table_secrets=secrets, skip_if_exists=True,
                existing_table=True)
            if (already_exists and
                self.table_spec(name) != table_spec):
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")

    def add_existing_snowflake_table(
        self,
        name: str,
        snowflake_user: str,
        snowflake_account: str,
        snowflake_database: str,
        snowflake_schema: str,
        snowflake_warehouse: str,
        snowflake_table_name: Optional[str] = None,
        snowflake_password: Optional[str] = None):
        """Adds a reference in this app to an existing Snowflake table.

        If using this method, Inductor must have been installed with
        Snowflake support enabled, as follows:
        `pip install --upgrade inductor[snowflake]`

        If a table is already referenced in this app under the given name, then
        it must have the characteristics specified by this method call's
        arguments; otherwise, this method raises an exception.

        Args:
            name: Name in this app under which to add a reference to the
                specified existing Snowflake table.
            snowflake_user: Snowflake username.
            snowflake_account: Snowflake account name.
            snowflake_database: Snowflake database name.
            snowflake_schema: Snowflake schema name.
            snowflake_warehouse: Snowflake warehouse name to use with this
                table.
            snowflake_table_name: Name of existing table in database given by
                preceding arguments. If not provided, the value of the name
                argument is used.
            snowflake_password: Optionally, password for user.  If not
                provided, password must be provided by secrets file.

        Raises:
            RuntimeError if a table having given name already exists but does
            not have the characteristics specified by this method call's
            arguments.
        """
        from inductor.data.table import snowflake  # pylint: disable=import-outside-toplevel

        if snowflake_table_name is None:
            snowflake_table_name = name

        table_spec = locals().copy()
        del table_spec["self"]

        if not self._run_time:
            self._table_creation_instructions.append(
                (self.add_existing_snowflake_table.__name__, table_spec))
            return

        del table_spec["snowflake_password"]
        password = (snowflake_password if snowflake_password is not None
                    else self._secrets.get(name, {}).get("snowflake_password"))
        if password is None:
            raise ValueError("No snowflake_password was provided for "
                             f"table {name}.")

        if name in self:
            if self.table_spec(name) != table_spec:
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")
        else:
            table_args = {
                "user": snowflake_user,
                "password": password,
                "account": snowflake_account,
                "database": snowflake_database,
                "schema": snowflake_schema,
                "warehouse": snowflake_warehouse,
                "table_name": snowflake_table_name,
                "auto_ddl": False,
            }
            secrets = None if snowflake_password is None else {
                "snowflake_password": snowflake_password
            }
            t = snowflake.SnowflakeTable(**table_args)
            already_exists = not self._add_table(
                name, t, table_spec, table_secrets=secrets, skip_if_exists=True,
                existing_table=True)
            if (already_exists and
                self.table_spec(name) != table_spec):
                raise RuntimeError(
                    f"Table {name} already exists but has different "
                    "table_spec.")

# Copyright 2022 Inductor, Inc.

"""Abstractions for PostgreSQL tables."""

import datetime
import re
import sys  # pylint: disable=unused-import
from typing import Any, Dict, Iterable, Optional, Tuple, Union

import psycopg2
from psycopg2 import errorcodes
from psycopg2 import extras

from inductor.data.table import table

# Name of empty placeholder column used to ensure that PostgreSQL tables never
# contain no columns
_PLACEHOLDER_COLUMN = "inductor_placeholder_column"

# Suffix appended to names of columns that thus far contain only null values.
_ALL_NULL_COLUMN_SUFFIX = "__allnull__"


def _clean_row_dict(row_dict: table.Row) -> table.Row:
    """Returns a copy of row_dict with modifications.

    Args:
        row: A raw row dictionary returned by a psycopg2.cursors.DictCursor.

    Returns:
        A new dictionary containing the same contents as row_dict, but with
        the following modifications:
            - The placeholder column, _PLACEHOLDER_COLUMN, is removed.
            - Columns with names ending in _ALL_NULL_COLUMN_SUFFIX are renamed
                to remove the suffix.
    """
    clean_row_dict = {}
    for key in row_dict.keys():
        if key != _PLACEHOLDER_COLUMN:
            if key.endswith(_ALL_NULL_COLUMN_SUFFIX):
                clean_row_dict[
                    key[:-len(_ALL_NULL_COLUMN_SUFFIX)]] = row_dict[key]
            else:
                clean_row_dict[key] = row_dict[key]
    return clean_row_dict


def _standardize_output(value: Any) -> Any:
    """Converts values from PostgreSQL to their original Python data types.

    Converts memoryview objects to bytes objects.

    Args:
        value: The value to convert.

    Returns:
        The converted value.
    """
    if isinstance(value, memoryview):
        return bytes(value)
    elif isinstance(value, dict):
        return {
            k: _standardize_output(v)
            for k, v in value.items()}
    elif isinstance(value, set):
        return set(
            _standardize_output(item)
            for item in value)
    elif isinstance(value, list):
        return [
            _standardize_output(item)
            for item in value]
    else:
        return value


def _format_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Formats metadata to have the right params for PostgresqlTable.

    Args:
        metadata: Metadata representing a PostgresqlTable.
    """
    table_metadata = metadata.copy()
    if "postgresql_password" in table_metadata:
        table_metadata["password"] = table_metadata["postgresql_password"]
        del table_metadata["postgresql_password"]
    return table_metadata


class PostgresqlView(table.Table):
    """A view of a PostgreSQL table."""

    def __init__(
        self,
        parent: "PostgresqlTable",
        query: table.SqlSelectQuery):
        """Constructs a new PostgresqlView instance.

        Args:
            parent: The underlying PostgresqlTable of which
                this instance is a view.
            query: The query (over parent) defining this view.
        """
        self._parent = parent
        self._query = query

    def _query_string(self) -> Tuple[str, Tuple[Any]]:
        """Returns the SQL query string and values underlying this view."""
        # pylint: disable-next=protected-access
        return self._query.to_sql_query_string(self._parent._table_name)

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        rows = []
        try:
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                cursor.execute(query_string, query_values)
                row_dict = cursor.fetchone()
                while row_dict is not None:
                    if self._parent._auto_ddl:  # pylint: disable=protected-access
                        row_dict = _clean_row_dict(row_dict)
                    row_dict = _standardize_output(row_dict)
                    rows.append(row_dict)
                    row_dict = cursor.fetchone()
            self._parent._connection.commit()  # pylint: disable=protected-access
        except psycopg2.Error as error:
            self._parent._connection.rollback()  # pylint: disable=protected-access
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                cursor.execute(
                    f"SELECT COUNT(*) AS c FROM {self._parent._table_name}")  # pylint: disable=protected-access
                total_num_rows = cursor.fetchone()["c"]
            self._parent._connection.commit()  # pylint: disable=protected-access
            if total_num_rows == 0:
                rows = []
            else:
                raise error
        return rows.__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        try:
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                cursor.execute(
                    f"SELECT * FROM ({query_string}) AS subquery LIMIT 1",
                    query_values)
                row_dict = cursor.fetchone()
            self._parent._connection.commit()  # pylint: disable=protected-access
        except psycopg2.Error as error:
            self._parent._connection.rollback()  # pylint: disable=protected-access
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                cursor.execute(
                    f"SELECT COUNT(*) AS c FROM {self._parent._table_name}")  # pylint: disable=protected-access
                total_num_rows = cursor.fetchone()["c"]
            self._parent._connection.commit()  # pylint: disable=protected-access
            if total_num_rows == 0:
                return None
            raise error
        if row_dict is not None:
            if self._parent._auto_ddl:  # pylint: disable=protected-access
                row_dict = _clean_row_dict(row_dict)
            row_dict = _standardize_output(row_dict)
        return row_dict

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        row = self.first_row()
        return list(row.keys()) if row is not None else []

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        return NotImplementedError()

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> table.Table:
        return NotImplementedError()


class PostgresqlTable(table.SqlQueryable, table.Appendable):
    """A Table backed by a PostgreSQL table."""

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        table_name: str,
        indexed_columns: Iterable[str] = tuple(),
        port: Optional[int] = None,
        auto_ddl: bool = True):
        """Constructs a new PostgresqlTable instance.

        Args:
            host: Name of database server host hosting the PostgreSQL database
                containing this table.
            user: PostgreSQL database server username.
            password: Password for user.
            database: Name of database containing table.
            table_name: Name of table in database given by preceding arguments.
            indexed_columns: Names of columns that should be indexed for faster
                queries.
            port: Optionally, the port on which to connect to the database
                server.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """
        self._connection_params = {
            "host": host, "user": user,
            "password": password, "database": database,
            "cursor_factory": extras.RealDictCursor
        }
        if port is not None:
            self._connection_params["port"] = port
        self._table_name = table_name
        self._indexed_columns = list(indexed_columns)
        self._auto_ddl = auto_ddl
        self._connection = psycopg2.connect(**self._connection_params)
        if self._auto_ddl:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self._table_name} "
                    f"({_PLACEHOLDER_COLUMN} INTEGER)")
            self._connection.commit()

    def __del__(self):
        """Closes self._connection as necessary on object destruction."""
        if (not self._connection.closed and
            # To ensure that the Python interpreter is not currently exiting
            # (self._connection.close() here may raise an exception if called
            # while interpreter is exiting).
            "sys" in globals() and
            hasattr("sys", "modules")):
            self._connection.close()

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        return PostgresqlView(self, table.SqlSelectQuery("*")).__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        return PostgresqlView(self, table.SqlSelectQuery("*")).first_row()

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        row = self.first_row()
        return list(row.keys()) if row is not None else []

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        metadata = self._connection_params.copy()
        del metadata["cursor_factory"]
        del metadata["password"]
        metadata["table_name"] = self._table_name
        metadata["indexed_columns"] = self._indexed_columns
        metadata["auto_ddl"] = self._auto_ddl
        return metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "PostgresqlTable":
        """See base class."""
        return PostgresqlTable(**_format_metadata(metadata))

    def indexed_columns(self) -> Iterable[str]:
        """See base class."""
        return self._indexed_columns.copy()

    def select(self, expression: str, after_from: str = "") -> PostgresqlView:
        """See base class."""
        return PostgresqlView(
            self,
            table.SqlSelectQuery(
                expression=expression, after_from=after_from, placeholder="%s"))

    def _add_table_columns(self, rows: Iterable[table.Row]):
        """Adds columns to underlying table for any new columns in rows.

        Args:
            rows: New rows based upon which to update table columns.
        """
        if not self._auto_ddl:
            return
        # Determine set of existing column names
        existing_col_names = set()
        with self._connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._table_name} LIMIT 0")
            for col in cursor.description:
                if col.name != _PLACEHOLDER_COLUMN:
                    existing_col_names.add(col.name)
        self._connection.commit()
        # Add table columns as necessary
        for row in rows:
            for col_name in row.keys():
                if (col_name not in existing_col_names
                    or (row[col_name] is not None and
                    col_name + _ALL_NULL_COLUMN_SUFFIX
                    in existing_col_names)):
                    if col_name == _PLACEHOLDER_COLUMN:
                        raise ValueError(
                            f"Cannot add a column having name equal to "
                            f"placeholder column name ({_PLACEHOLDER_COLUMN}).")
                    elif col_name.endswith(_ALL_NULL_COLUMN_SUFFIX):
                        raise ValueError(
                            f"Column names cannot end with "
                            f"\"{_ALL_NULL_COLUMN_SUFFIX}\" "
                            f"(encountered column name {col_name}).")
                    elif not re.match(r"\A[a-zA-Z0-9_]+\Z", col_name):
                        raise ValueError(
                            "Column names must match "
                            r"\A[a-zA-Z0-9_]+\Z "
                            f"(encountered column name {col_name}).")
                    value = row[col_name]
                    if value is None:
                        # Create two columns: col_name and col_name_all_null
                        col_name_all_null = col_name + _ALL_NULL_COLUMN_SUFFIX
                        with self._connection.cursor() as cursor:
                            cursor.execute(
                                f"ALTER TABLE {self._table_name} ADD COLUMN "
                                f"{col_name} TEXT DEFAULT NULL")
                            cursor.execute(
                                f"ALTER TABLE {self._table_name} ADD COLUMN "
                                f"{col_name_all_null} TEXT DEFAULT NULL")
                        existing_col_names.add(col_name)
                        existing_col_names.add(col_name_all_null)
                    else:
                        if isinstance(value, bool):
                            postgresql_type = "BOOLEAN"
                        elif isinstance(value, int):
                            postgresql_type = "INTEGER"
                        elif isinstance(value, float):
                            postgresql_type = "DOUBLE PRECISION"
                        elif isinstance(value, str):
                            postgresql_type = "TEXT"
                        elif isinstance(value, bytes):
                            postgresql_type = "BYTEA"
                        elif isinstance(value, datetime.datetime):
                            postgresql_type = "TIMESTAMP"
                        elif isinstance(value, datetime.date):
                            postgresql_type = "DATE"
                        else:
                            raise TypeError(
                                f"Unsupported value type: {type(value)}")
                        with self._connection.cursor() as cursor:
                            if col_name in existing_col_names:
                                cursor.execute(
                                    f"ALTER TABLE {self._table_name} "
                                    f"DROP COLUMN "
                                    f"{col_name + _ALL_NULL_COLUMN_SUFFIX}")
                                existing_col_names.remove(
                                    col_name + _ALL_NULL_COLUMN_SUFFIX)
                                cursor.execute(
                                    f"ALTER TABLE {self._table_name} "
                                    f"ALTER COLUMN {col_name} "
                                    f"TYPE {postgresql_type} "
                                    f"USING {col_name}::{postgresql_type}")
                            else:
                                cursor.execute(
                                    f"ALTER TABLE {self._table_name} "
                                    f"ADD COLUMN {col_name} {postgresql_type} "
                                    "DEFAULT NULL")
                                existing_col_names.add(col_name)
                                if (col_name + _ALL_NULL_COLUMN_SUFFIX in
                                    existing_col_names):
                                    cursor.execute(
                                        f"ALTER TABLE {self._table_name} "
                                        "DROP COLUMN "
                                        f"{col_name + _ALL_NULL_COLUMN_SUFFIX}")
                                    existing_col_names.remove(
                                        col_name + _ALL_NULL_COLUMN_SUFFIX)
                            if col_name in self._indexed_columns:
                                cursor.execute(
                                    "CREATE INDEX "
                                    f"{self._table_name}__{col_name}_index "
                                    f"ON {self._table_name} "
                                    f"({col_name})")
                            if (isinstance(self, PostgresqlKeyedTable) and
                                # pylint: disable=no-member
                                col_name == self.primary_key_column()):
                                # pylint: enable=no-member
                                cursor.execute(
                                    f"ALTER TABLE {self._table_name} "
                                    f"ADD PRIMARY KEY ({col_name})")
                        self._connection.commit()

    def extend(self, rows: Iterable[table.Row]):
        """See base class."""
        self._add_table_columns(rows)
        with self._connection.cursor() as cursor:
            for row in rows:
                all_values_none = all(value is None for value in row.values())
                if all_values_none:
                    cursor.execute(
                        f"INSERT INTO {self._table_name} "
                        f"DEFAULT VALUES")
                else:
                    col_names = [k for k, v in row.items() if v is not None]
                    col_names_clause = ",".join(col_names)
                    values_clause = ",".join(["%s" for _ in col_names])
                    cursor.execute(
                        f"INSERT INTO {self._table_name} "
                        f"({col_names_clause}) "
                        f"VALUES({values_clause})",
                        tuple(row[c] for c in col_names))
        self._connection.commit()


class PostgresqlKeyedTable(PostgresqlTable, table.WithPrimaryKey):
    """A PostgresqlTable having a primary key."""

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        table_name: str,
        primary_key_column: str,
        indexed_columns: Iterable[str] = tuple(),
        port: Optional[int] = None,
        auto_ddl: bool = True):
        """Constructs a new PostgresqlKeyedTable instance.

        Args:
            host: Name of database server host hosting the PostgreSQL database
                containing this table.
            user: PostgreSQL database server username.
            password: Password for user.
            database: Name of database containing table.
            table_name: Name of table in database given by preceding arguments.
            primary_key_column: Name of column containing primary key.
            indexed_columns: Names of columns that should be indexed for faster
                queries.
            port: Optionally, the port on which to connect to the database
                server.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """
        super().__init__(
            host=host, user=user, password=password, database=database,
            table_name=table_name, indexed_columns=indexed_columns, port=port,
            auto_ddl=auto_ddl)
        self._primary_key_column = primary_key_column

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        super_metadata = super().to_metadata()
        if "primary_key_column" in super_metadata:
            raise RuntimeError(
                "super_metadata already contains key \"primary_key_column\".")
        super_metadata["primary_key_column"] = self._primary_key_column
        return super_metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "PostgresqlKeyedTable":
        """See base class."""
        return PostgresqlKeyedTable(**_format_metadata(metadata))

    def extend(self, rows: Iterable[table.Row]):
        """See base class.

        All rows in rows must contain a primary key in the column named
        self.primary_key_column().
        """
        for row in rows:
            if (self._primary_key_column not in row
                or row[self._primary_key_column] is None):
                raise ValueError(
                    f"All rows in rows must contain a primary key in the "
                    f"column named {self._primary_key_column}.")

        self._add_table_columns(rows)

        # Extend the table using the `INSERT INTO... ON CONFLICT DO UPDATE SET`
        # statement in order to avoid duplicate primary keys. This will have
        # the same effect as `REPLACE INTO` in MySQL or SQLite, but requires
        # including all columns in the `INSERT` statement, even if they are
        # not being updated.
        columns_in_rows = set()
        for row in rows:
            for col in row.keys():
                columns_in_rows.add(col)
        all_columns = list(set(self.columns).union(columns_in_rows))
        with self._connection.cursor() as cursor:
            for row in rows:
                col_names_clause = ",".join(all_columns)
                values_clause = ""
                parameters = []
                for col in all_columns:
                    if col in row:
                        values_clause += "%s,"
                        parameters.append(row[col])
                    else:
                        values_clause += "DEFAULT,"
                values_clause = values_clause[:-1]

                set_clause = ",".join(f"{c}=EXCLUDED.{c}" for c in all_columns)

                cursor.execute(
                    f"INSERT INTO {self._table_name} "
                    f"({col_names_clause}) "
                    f"VALUES({values_clause}) "
                    f"ON CONFLICT ({self._primary_key_column}) "
                    f"DO UPDATE SET {set_clause}",
                    parameters)
        self._connection.commit()

    def primary_key_column(self) -> str:
        """See base class."""
        return self._primary_key_column

    def get(
        self,
        key: Any,
        default: Optional[table.Row] = None) -> Optional[table.Row]:
        """See base class."""
        with self._connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"SELECT * FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=%s", (key,))
                table_rows = cursor.fetchall()
                self._connection.commit()
            except psycopg2.Error as error:
                self._connection.rollback()
                if error.pgcode == errorcodes.UNDEFINED_COLUMN:
                    table_rows = None
                else:
                    raise error
        if not table_rows:
            return default
        if len(table_rows) > 1:
            raise RuntimeError("Found multiple rows having same primary key.")
        table_row = table_rows[0]
        if self._auto_ddl:
            table_row = _clean_row_dict(table_row)
        table_row = _standardize_output(table_row)
        return table_row

    def __contains__(self, key: Any) -> bool:
        """See base class."""
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT COUNT(*) AS c FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=%s", (key,))
                c = cursor.fetchone()["c"]
            self._connection.commit()
            return c > 0
        except psycopg2.Error as error:
            self._connection.rollback()
            with self._connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) AS c FROM {self._table_name}")
                total_num_rows = cursor.fetchone()["c"]
            self._connection.commit()
            if total_num_rows == 0:
                return False
            else:
                raise error

    def set(
        self, key: Any, row: table.Row, skip_if_exists: bool = False) -> bool:
        """See base class.

        Primary key value cannot be None.
        """
        # Ensure that key is not None
        if key is None:
            raise ValueError("Primary key value cannot be None.")
        # Ensure that row contains primary key value
        if self._primary_key_column in row:
            if key != row[self._primary_key_column]:
                raise ValueError(
                    "Primary key value in row does not match key argument.")
        else:
            row = row.copy()
            row[self._primary_key_column] = key
        # Add any new table columns
        self._add_table_columns([row])
        # Insert or replace row
        with self._connection.cursor() as cursor:
            if not skip_if_exists:
                cursor.execute(
                    f"DELETE FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=%s", (key,))
            col_names = [k for k, v in row.items() if v is not None]
            col_names_clause = ",".join(col_names)
            values_clause = ",".join(["%s" for _ in col_names])
            if skip_if_exists:
                on_conflict_key_clause = "ON CONFLICT DO NOTHING"
            else:
                on_conflict_key_clause = ""
            cursor.execute(
                (f"INSERT INTO {self._table_name} ({col_names_clause}) " +
                f"VALUES({values_clause}) {on_conflict_key_clause}"),
                tuple(row[c] for c in col_names))
            if skip_if_exists:
                rc = cursor.rowcount
                return_value = rc is not None and rc > 0
            else:
                return_value = True
        self._connection.commit()
        return return_value

    def update(self, key: Any, values: table.Row):
        """See base class.

        Primary key value cannot be None.
        """
        # Ensure that key is not None
        if key is None:
            raise ValueError("Primary key value cannot be None.")
        # Ensure that values contains a primary key value
        if self._primary_key_column in values:
            if key != values[self._primary_key_column]:
                raise ValueError(
                    "Primary key value in values does not match key argument.")
        else:
            values = values.copy()
            values[self._primary_key_column] = key
        # Add any new table columns
        self._add_table_columns([values])
        # Insert or update values
        # (Note: We only insert or update values for columns that explicitly
        # exist in the table, as, by virtue of the preceding call to
        # self._add_table_columns(), all other values must be None in the values
        # argument and are already null in the table.)
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._table_name} ({self._primary_key_column}) "
                f"VALUES(%s) ON CONFLICT DO NOTHING", (key,))
            # We do not update a column that is null/None in the values
            #   argument and all null/None in the table. Therefore we
            #   use the raw columns (that contain _ALL_NULL_COLUMN_SUFFIX
            #   suffixes) to determine which columns to update.
            existing_col_names = set()
            cursor.execute(f"SELECT * FROM {self._table_name} LIMIT 0")
            for col in cursor.description:
                if not self._auto_ddl or col.name != _PLACEHOLDER_COLUMN:
                    existing_col_names.add(col.name)
            update_col_names = [
                k for k in values.keys() if k in existing_col_names]
            set_clause = ",".join([f"{c}=%s" for c in update_col_names])
            cursor.execute(
                f"UPDATE {self._table_name} SET {set_clause} "
                f"WHERE {self._primary_key_column}=%s",
                tuple([values[c] for c in update_col_names] + [key]))
        self._connection.commit()

    def __delitem__(self, key: Any):
        """See base class."""
        with self._connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"DELETE FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=%s", (key,))
            except psycopg2.Error as error:
                self._connection.rollback()
                if error.pgcode == errorcodes.UNDEFINED_COLUMN:
                    pass
                else:
                    raise error
        self._connection.commit()

    def increment(
        self,
        key: Any,
        column_name: str,
        increment_by: int) -> Union[int, float]:
        """See base class."""
        # Ensure that key is not None.
        if key is None:
            raise ValueError("Primary key value cannot be None.")
        # Ensure that the column_name is not the primary key column.
        if column_name == self._primary_key_column:
            raise ValueError("Cannot increment primary key column.")
        # Increment column.
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"UPDATE {self._table_name} "
                    f"SET {column_name}={column_name}+%s "
                    f"WHERE {self._primary_key_column}=%s",
                    (increment_by, key))
                cursor.execute(
                    f"SELECT {column_name} FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=%s", (key,))
                value_updated = cursor.fetchone()
        except psycopg2.Error as error:
            self._connection.rollback()
            if (error.pgcode in (errorcodes.UNDEFINED_COLUMN,
                                 errorcodes.UNDEFINED_FUNCTION)):
                value_updated = None
            else:
                raise error
        else:
            self._connection.commit()

        if value_updated is None:
            raise ValueError(f"Column {column_name} or key {key} does not"
                             f"exist in table {self._table_name}.")
        return value_updated[column_name]

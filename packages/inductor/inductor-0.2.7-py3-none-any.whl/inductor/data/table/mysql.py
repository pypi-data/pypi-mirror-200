# Copyright 2022 Inductor, Inc.

"""Abstractions for MySQL tables."""

import datetime
import re
import sys  # pylint: disable=unused-import
from typing import Any, Dict, Iterable, Optional, Tuple, Union

import pymysql

from inductor.data.table import table

# Name of empty placeholder column used to ensure that MySQL tables never
# contain no columns
_PLACEHOLDER_COLUMN = "inductor_placeholder_column"

# Suffix appended to names of columns that thus far contain only null values.
_ALL_NULL_COLUMN_SUFFIX = "__allnull__"


def _clean_row_dict(row_dict: table.Row) -> table.Row:
    """Cleans a raw row dictionary returned by a pymysql.cursors.DictCursor.

    Args:
        row: A raw row dictionary returned by a pymysql.cursors.DictCursor.

    Returns:
        A new dictionary containing the cleaned contents of row_dict.
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


def _format_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Formats metadata to have the right params for MysqlTable.

    Args:
        metadata: Metadata representing a MysqlTable.
    """
    table_metadata = metadata.copy()
    if "mysql_password" in table_metadata:
        table_metadata["password"] = table_metadata["mysql_password"]
        del table_metadata["mysql_password"]
    return table_metadata


class MysqlView(table.Table):
    """A view of a MySQL table."""

    def __init__(
        self,
        parent: "MysqlTable",
        query: table.SqlSelectQuery):
        """Constructs a new MysqlView instance.

        Args:
            parent: The underlying MysqlTable of which this instance is a view.
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
            with self._parent._connection.cursor() as cursor:
                cursor.execute(query_string, query_values)
                row_dict = cursor.fetchone()
                while row_dict is not None:
                    if self._parent._auto_ddl:  # pylint: disable=protected-access
                        row_dict = _clean_row_dict(row_dict)
                    rows.append(row_dict)
                    row_dict = cursor.fetchone()
            self._parent._connection.commit()  # pylint: disable=protected-access
        except pymysql.MySQLError as error:
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
        try:
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                query_string, query_values = self._query_string()
                cursor.execute(
                    f"SELECT * FROM ({query_string}) AS subquery LIMIT 1",
                    query_values)
                row_dict = cursor.fetchone()
            self._parent._connection.commit()  # pylint: disable=protected-access
        except pymysql.MySQLError as error:
            self._parent._connection.rollback()  # pylint: disable=protected-access
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                cursor.execute(
                    f"SELECT COUNT(*) AS c FROM {self._parent._table_name}")  # pylint: disable=protected-access
                total_num_rows = cursor.fetchone()["c"]
            self._parent._connection.commit()  # pylint: disable=protected-access
            if total_num_rows == 0:
                return None
            raise error
        if row_dict is not None and self._parent._auto_ddl:  # pylint: disable=protected-access
            row_dict = _clean_row_dict(row_dict)
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


class MysqlTable(table.SqlQueryable, table.Appendable):
    """A Table backed by a MySQL table."""

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
        """Constructs a new MysqlTable instance.

        Args:
            host: Name of database server host hosting the MySQL database
                containing this table.
            user: MySQL database server username.
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
            "cursorclass": pymysql.cursors.DictCursor
        }
        if port:
            self._connection_params["port"] = port
        self._table_name = table_name
        self._indexed_columns = list(indexed_columns)
        self._auto_ddl = auto_ddl
        self._connection = pymysql.connect(**self._connection_params)
        if self._auto_ddl:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self._table_name} "
                    f"({_PLACEHOLDER_COLUMN} INTEGER)")
            self._connection.commit()

    def __del__(self):
        """Closes self._connection as necessary on object destruction."""
        if (self._connection.open and
            # To ensure that the Python interpreter is not currently exiting
            # (self._connection.close() here raises an exception if called while
            # interpreter is exiting).
            "sys" in globals() and
            hasattr("sys", "modules")):
            self._connection.close()

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        return MysqlView(self, table.SqlSelectQuery("*")).__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        return MysqlView(self, table.SqlSelectQuery("*")).first_row()

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        row = self.first_row()
        return list(row.keys()) if row is not None else []

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        metadata = self._connection_params.copy()
        del metadata["cursorclass"]
        del metadata["password"]
        metadata["table_name"] = self._table_name
        metadata["indexed_columns"] = self._indexed_columns
        metadata["auto_ddl"] = self._auto_ddl
        return metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "MysqlTable":
        """See base class."""
        return MysqlTable(**_format_metadata(metadata))

    def indexed_columns(self) -> Iterable[str]:
        """See base class."""
        return self._indexed_columns.copy()

    def select(self, expression: str, after_from: str = "") -> MysqlView:
        """See base class."""
        return MysqlView(
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
            cursor.execute(f"SHOW COLUMNS FROM {self._table_name}")
            for row in cursor.fetchall():
                col_name = row["Field"]
                if col_name != _PLACEHOLDER_COLUMN:
                    existing_col_names.add(col_name)
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
                        index_prefix_clause = ""
                        if isinstance(value, bool):
                            mysql_type = "BOOLEAN"
                        elif isinstance(value, int):
                            mysql_type = "INTEGER"
                        elif isinstance(value, float):
                            mysql_type = "DOUBLE"
                        elif isinstance(value, str):
                            mysql_type = "TEXT"
                            index_prefix_clause = "(300)"
                            if (isinstance(self, MysqlKeyedTable) and
                                # pylint: disable-next=no-member
                                col_name == self.primary_key_column()):
                                mysql_type = "VARCHAR(255)"
                                index_prefix_clause = "(255)"
                        elif isinstance(value, bytes):
                            mysql_type = "BLOB"
                            index_prefix_clause = "(600)"
                        elif isinstance(value, datetime.datetime):
                            mysql_type = "DATETIME"
                        elif isinstance(value, datetime.date):
                            mysql_type = "DATE"
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
                                    f"CHANGE COLUMN {col_name} "
                                    f"{col_name} {mysql_type} "
                                    "DEFAULT NULL")
                            else:
                                if (isinstance(self, MysqlKeyedTable) and
                                    # pylint: disable-next=no-member
                                    col_name == self.primary_key_column()):
                                    cursor.execute(
                                        f"ALTER TABLE {self._table_name} "
                                        f"ADD COLUMN {col_name} {mysql_type}")
                                else:
                                    cursor.execute(
                                        f"ALTER TABLE {self._table_name} "
                                        f"ADD COLUMN {col_name} {mysql_type} "
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
                                    f"({col_name}{index_prefix_clause})")
                            if (isinstance(self, MysqlKeyedTable) and
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
                col_names = [k for k, v in row.items() if v is not None]
                col_names_clause = ",".join(col_names)
                values_clause = ",".join(["%s" for _ in col_names])
                cursor.execute(
                    f"REPLACE INTO {self._table_name} "
                    f"({col_names_clause}) "
                    f"VALUES({values_clause})",
                    tuple(row[c] for c in col_names))
        self._connection.commit()


class MysqlKeyedTable(MysqlTable, table.WithPrimaryKey):
    """A MysqlTable having a primary key."""

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
        """Constructs a new MysqlKeyedTable instance.

        Args:
            host: Name of database server host hosting the MySQL database
                containing this table.
            user: MySQL database server username.
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
    def from_metadata(metadata: Dict[str, Any]) -> "MysqlKeyedTable":
        """See base class."""
        return MysqlKeyedTable(**_format_metadata(metadata))

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
        # Note that super().extend() creates the primary key column in the
        # underlying table if it does not already exist.
        super().extend(rows)

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
            except pymysql.MySQLError as error:
                self._connection.rollback()
                if (error.args[0] == pymysql.constants.ER.BAD_FIELD_ERROR
                        and "Unknown column" in error.args[1]):
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
        except pymysql.MySQLError as error:
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
                on_duplicate_key_clause = (
                    "ON DUPLICATE KEY UPDATE "
                    f"{self._primary_key_column}={self._primary_key_column}")
            else:
                on_duplicate_key_clause = ""
            cursor.execute(
                (f"INSERT INTO {self._table_name} ({col_names_clause}) " +
                f"VALUES({values_clause}) {on_duplicate_key_clause}"),
                tuple(row[c] for c in col_names))
            if skip_if_exists:
                cursor.execute("SELECT ROW_COUNT() AS rc")
                return_value = cursor.fetchone()["rc"] > 0
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
                f"VALUES(%s) ON DUPLICATE KEY UPDATE "
                f"{self._primary_key_column}={self._primary_key_column}",
                (key,))
            existing_col_names = set()
            cursor.execute(f"SELECT * FROM {self._table_name} LIMIT 1")
            for row in cursor.fetchall():
                for col_name in row.keys():
                    if not self._auto_ddl or col_name != _PLACEHOLDER_COLUMN:
                        existing_col_names.add(col_name)
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
            except pymysql.MySQLError as error:
                self._connection.rollback()
                if (error.args[0] == pymysql.constants.ER.BAD_FIELD_ERROR
                    and "Unknown column" in error.args[1]):
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
            raise ValueError(
                "Cannot increment primary key column.")
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
        except pymysql.MySQLError as error:
            self._connection.rollback()
            if (error.args[0] == pymysql.constants.ER.BAD_FIELD_ERROR
                and "Unknown column" in error.args[1]):
                value_updated = None
            else:
                raise error
        else:
            self._connection.commit()

        if value_updated is None:
            raise ValueError(
                f"Column {column_name} does not exist in table "
                f"{self._table_name}.")
        return value_updated[column_name]

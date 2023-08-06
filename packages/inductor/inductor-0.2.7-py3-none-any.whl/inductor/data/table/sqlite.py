# Copyright 2022 Inductor, Inc.

"""Abstractions for sqlite tables."""

import datetime
import os
import re
import sqlite3
from typing import Any, Dict, Iterable, Optional, Tuple, Union

from inductor.data.table import table

# Name of empty placeholder column used to ensure that sqlite tables never
# contain no columns
_PLACEHOLDER_COLUMN = "inductor_placeholder_column"

# Reserved column name suffix used in other database system implementations.
_ALL_NULL_COLUMN_SUFFIX = "_all_null"


def _row_to_row_dict(clean: bool, row: sqlite3.Row) -> table.Row:
    """Converts a raw sqlite3.Row to the corresponding table.Row.

    Args:
        clean: Boolean value indicating whether or not to clean the row.
        row: A sqlite3.Row returned by a sqlite query.

    Returns:
        A table.Row containing the contents of row, transformed as necessary.
    """
    row_dict = {}
    for key in row.keys():
        if not clean or key != _PLACEHOLDER_COLUMN:
            row_dict[key] = row[key]
    return row_dict


def _standardize_output(value: Any) -> Any:
    """Converts values from SQLite to their original Python data types.

    Converts isoformatted strings to datetime/date objects.

    Args:
        value: The value to convert.

    Returns:
        The converted value.
    """
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value)
        except ValueError:
            pass
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError:
            pass
        return value
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


class SqliteView(table.Table):
    """A view of a sqlite table."""

    def __init__(
        self,
        parent: "SqliteTable",
        query: table.SqlSelectQuery):
        """Constructs a new SqliteView instance.

        Args:
            parent: The underlying SqliteTable of which this instance is a view.
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
            for row in self._parent._connection.execute(
                query_string, query_values):
                # pylint: disable-next=protected-access
                row_dict = _row_to_row_dict(self._parent._auto_ddl, row)
                rows.append(_standardize_output(row_dict))
        except sqlite3.Error as error:
            self._parent._connection.rollback()  # pylint: disable=protected-access
            total_num_rows = self._parent._connection.execute(  # pylint: disable=protected-access
                f"SELECT COUNT(*) FROM {self._parent._table_name}"  # pylint: disable=protected-access
            ).fetchone()[0]
            self._parent._connection.commit()  # pylint: disable=protected-access
            if total_num_rows == 0:
                rows = []
            else:
                raise error
        return rows.__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        query_string = (
            f"WITH view_rows AS ({query_string}) "
            f"SELECT * FROM view_rows LIMIT 1")
        try:
            # pylint: disable-next=protected-access
            for row in self._parent._connection.execute(
                query_string, query_values):
                # pylint: disable-next=protected-access
                row_dict = _row_to_row_dict(self._parent._auto_ddl, row)
                row_dict = _standardize_output(row_dict)
                return row_dict
        except sqlite3.Error as error:
            self._parent._connection.rollback()  # pylint: disable=protected-access
            total_num_rows = self._parent._connection.execute(  # pylint: disable=protected-access
                f"SELECT COUNT(*) FROM {self._parent._table_name}"  # pylint: disable=protected-access
            ).fetchone()[0]
            self._parent._connection.commit()  # pylint: disable=protected-access
            if total_num_rows != 0:
                raise error
        return None

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


class SqliteTable(table.SqlQueryable, table.Appendable):
    """A Table backed by a sqlite table."""

    def __init__(
        self,
        db_file_path: str,
        table_name: str,
        indexed_columns: Iterable[str] = tuple(),
        auto_ddl: bool = True):
        """Constructs a new SqliteTable instance.

        Args:
            db_file_path: Path to file containing sqlite database in which
                this table is, or should be, stored.
            table_name: Name of table in file given by db_file_path.
            indexed_columns: Names of columns that should be indexed for fast
                range queries.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """
        self._db_file_path = db_file_path
        self._table_name = table_name
        self._indexed_columns = list(indexed_columns)
        self._auto_ddl = auto_ddl
        # It is possible to run SQLite in-memory,
        # in which case a filepath won't exist
        if db_file_path != ":memory:":
            os.makedirs(os.path.dirname(db_file_path), exist_ok=True)
        self._connection = sqlite3.connect(
            self._db_file_path,
            detect_types=sqlite3.PARSE_DECLTYPES)
        self._connection.row_factory = sqlite3.Row
        if self._auto_ddl:
            self._connection.execute(
                f"CREATE TABLE IF NOT EXISTS {self._table_name} "
                f"({_PLACEHOLDER_COLUMN} INTEGER)")
            self._connection.commit()

    def __del__(self):
        """Closes self._connection on object destruction."""
        self._connection.close()

    @property
    def db_file_path(self) -> str:
        """Returns path to file containing this sqlite database."""
        return self._db_file_path

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        return SqliteView(self, table.SqlSelectQuery("*")).__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        return SqliteView(self, table.SqlSelectQuery("*")).first_row()

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        row = self.first_row()
        return list(row.keys()) if row is not None else []

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        return {
            "db_file_path": self._db_file_path,
            "table_name": self._table_name,
            "indexed_columns": self._indexed_columns,
            "auto_ddl": self._auto_ddl,
        }

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "SqliteTable":
        """See base class."""
        return SqliteTable(**metadata)

    def indexed_columns(self) -> Iterable[str]:
        """See base class."""
        return self._indexed_columns.copy()

    def select(self, expression: str, after_from: str = "") -> SqliteView:
        """See base class."""
        return SqliteView(
            self,
            table.SqlSelectQuery(
                expression=expression, after_from=after_from, placeholder="?"))

    def _add_table_columns(self, rows: Iterable[table.Row]):
        """Adds columns to underlying table for any new columns in rows.

        Args:
            rows: New rows based upon which to update table columns.
        """
        if not self._auto_ddl:
            return
        # Determine set of existing column names
        existing_col_names = set()
        cursor = self._connection.execute(
            f"SELECT * FROM {self._table_name} LIMIT 1")
        for column in cursor.description:
            if column[0] != _PLACEHOLDER_COLUMN:
                existing_col_names.add(column[0])
        # Add table columns as necessary
        for row in rows:
            for col_name in row.keys():
                if col_name not in existing_col_names:
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
                        cursor = self._connection.cursor()
                        cursor.execute(
                            f"ALTER TABLE {self._table_name} ADD COLUMN "
                            f"{col_name}")
                        existing_col_names.add(col_name)
                        self._connection.commit()
                    else:
                        if isinstance(value, int):
                            sqlite_type = "INTEGER"
                        elif isinstance(value, float):
                            sqlite_type = "REAL"
                        elif isinstance(value, str):
                            sqlite_type = "TEXT"
                        elif isinstance(value, bytes):
                            sqlite_type = "BLOB"
                        elif isinstance(value, datetime.datetime):
                            sqlite_type = "TIMESTAMP"
                        elif isinstance(value, datetime.date):
                            sqlite_type = "DATE"
                        else:
                            raise TypeError(
                                f"Unsupported value type: {type(value)}")
                        cursor = self._connection.cursor()
                        cursor.execute(
                            f"ALTER TABLE {self._table_name} "
                            f"ADD COLUMN {col_name} {sqlite_type} "
                            "DEFAULT NULL")
                        existing_col_names.add(col_name)
                        if col_name in self._indexed_columns:
                            cursor.execute(
                                "CREATE INDEX "
                                f"{self._table_name}__{col_name}_index "
                                f"ON {self._table_name} ({col_name})")
                        if (isinstance(self, SqliteKeyedTable) and
                            # pylint: disable=no-member
                            col_name == self.primary_key_column()):
                            # pylint: enable=no-member
                            cursor.execute(
                                "CREATE UNIQUE INDEX "
                                f"{self._table_name}__"
                                f"{col_name}_primary_key_index "
                                f"ON {self._table_name} ({col_name})")
                        self._connection.commit()

    def extend(self, rows: Iterable[table.Row]):
        """See base class."""
        self._add_table_columns(rows)
        cursor = self._connection.cursor()
        for row in rows:
            all_values_none = all(value is None for value in row.values())
            if all_values_none:
                cursor.execute(
                    f"INSERT INTO {self._table_name} "
                    f"DEFAULT VALUES")
            else:
                col_names = [k for k, v in row.items() if v is not None]
                col_names_clause = ",".join(col_names)
                values_clause = ",".join(["?" for _ in col_names])
                cursor.execute(
                    f"REPLACE INTO {self._table_name} ({col_names_clause}) "
                    f"VALUES({values_clause})",
                    tuple(row[c] for c in col_names))
        self._connection.commit()


class SqliteKeyedTable(SqliteTable, table.WithPrimaryKey):
    """A SqliteTable having a primary key."""

    def __init__(
        self,
        db_file_path: str,
        table_name: str,
        primary_key_column: str,
        indexed_columns: Iterable[str] = tuple(),
        auto_ddl: bool = True):
        """Constructs a new SqliteKeyedTable instance.

        Args:
            db_file_path: Path to file containing sqlite database in which
                this table is, or should be, stored.
            table_name: Name of table in file given by db_file_path.
            primary_key_column: Name of column containing primary key.
            indexed_columns: Names of columns that should be indexed for fast
                range queries.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """
        super().__init__(
            db_file_path=db_file_path,
            table_name=table_name,
            indexed_columns=indexed_columns,
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
    def from_metadata(metadata: Dict[str, Any]) -> "SqliteKeyedTable":
        """See base class."""
        return SqliteKeyedTable(**metadata)

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
        try:
            table_rows = self._connection.execute(
                f"SELECT * FROM {self._table_name} "
                f"WHERE {self._primary_key_column}=?", (key,)).fetchall()
        except sqlite3.Error as error:
            self._connection.rollback()
            if "no such column" in str(error):
                return default
            raise error
        self._connection.commit()
        if not table_rows:
            return default
        if len(table_rows) > 1:
            raise RuntimeError("Found multiple rows having same primary key.")
        table_row = table_rows[0]
        table_row = _row_to_row_dict(self._auto_ddl, table_row)
        table_row = _standardize_output(table_row)
        return table_row

    def __contains__(self, key: Any) -> bool:
        """See base class."""
        try:
            return self._connection.execute(
                f"SELECT COUNT(*) FROM {self._table_name} "
                f"WHERE {self._primary_key_column}=?", (key,)).fetchone()[0] > 0
        except sqlite3.Error as error:
            self._connection.rollback()
            total_num_rows = self._connection.execute(
                f"SELECT COUNT(*) FROM {self._table_name}").fetchone()[0]
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
        cursor = self._connection.cursor()
        if not skip_if_exists:
            cursor.execute(
                f"DELETE FROM {self._table_name} "
                f"WHERE {self._primary_key_column}=?", (key,))
        col_names = [k for k, v in row.items() if v is not None]
        col_names_clause = ",".join(col_names)
        values_clause = ",".join(["?" for _ in col_names])
        cursor.execute(
            (f"INSERT INTO {self._table_name} ({col_names_clause}) " +
             f"VALUES({values_clause}) " +
             ("ON CONFLICT DO NOTHING" if skip_if_exists else "")),
             tuple(row[c] for c in col_names))
        if skip_if_exists:
            return_value = cursor.execute("SELECT changes()").fetchone()[0] > 0
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
        cursor = self._connection.cursor()
        cursor.execute(
            f"INSERT INTO {self._table_name} ({self._primary_key_column}) "
            f"VALUES(?) ON CONFLICT DO NOTHING", (key,))
        existing_col_names = set()
        for row in cursor.execute(
            f"SELECT * FROM {self._table_name} LIMIT 1"):
            for col_name in row.keys():
                if not self._auto_ddl or col_name != _PLACEHOLDER_COLUMN:
                    existing_col_names.add(col_name)
        update_col_names = [k for k in values.keys() if k in existing_col_names]
        set_clause = ",".join([f"{c}=?" for c in update_col_names])
        cursor.execute(
            f"UPDATE {self._table_name} SET {set_clause} "
            f"WHERE {self._primary_key_column}=?",
            tuple([values[c] for c in update_col_names] + [key]))
        self._connection.commit()

    def __delitem__(self, key: Any):
        """See base class."""
        try:
            self._connection.execute(
                f"DELETE FROM {self._table_name} "
                f"WHERE {self._primary_key_column}=?", (key,))
        except sqlite3.Error as error:
            self._connection.rollback()
            if "no such column" not in str(error):
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
        cursor = self._connection.cursor()
        try:
            cursor.execute(
                f"UPDATE {self._table_name} "
                f"SET {column_name}={column_name}+? "
                f"WHERE {self._primary_key_column}=?", (increment_by, key))
            cursor.execute(
                f"SELECT {column_name} FROM {self._table_name} "
                f"WHERE {self._primary_key_column}=?", (key,))
            value_updated = cursor.fetchone()
        except sqlite3.Error as error:
            self._connection.rollback()
            if "no such column" in str(error):
                value_updated = None
            else:
                raise error
        else:
            self._connection.commit()

        if value_updated is None:
            raise ValueError(
                f"Column {column_name} does not exist in table "
                f"{self._table_name}.")
        return value_updated[0]

# Copyright 2022 Inductor, Inc.

"""Abstractions for Snowflake tables."""

import datetime
import re
import sys  # pylint: disable=unused-import
from typing import Any, Dict, Iterable, Optional, Tuple

import pandas as pd
from snowflake import connector

from inductor.data.table import table


# Name of empty placeholder column used to ensure that Snowflake tables never
# contain no columns
_PLACEHOLDER_COLUMN = "inductor_placeholder_column"

# Suffix appended to names of columns that thus far contain only null values.
_ALL_NULL_COLUMN_SUFFIX = "__allnull__"


def _clean_row_dict(row_dict: table.Row) -> table.Row:
    """Returns a copy of row_dict with modifications.

    Args:
        row: A raw row dictionary returned by a Snowflake connector.

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
    """Converts values from Snowflake to their original Python data types.

    Converts bytearray objects to bytes objects.
    """
    if isinstance(value, bytearray):
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
    """Formats metadata to have the right params for SnowflakeTable.

    Args:
        metadata: Metadata representing a SnowflakeTable.
    """
    table_metadata = metadata.copy()
    if "snowflake_password" in table_metadata:
        table_metadata["password"] = table_metadata["snowflake_password"]
        del table_metadata["snowflake_password"]
    return table_metadata


class SnowflakeView(table.Table):
    """A view of a Snowflake table."""

    def __init__(
        self,
        parent: "SnowflakeTable",
        query: table.SqlSelectQuery):
        """Constructs a new SnowflakeView instance.

        Args:
            parent: The underlying SnowflakeTable of which
                this instance is a view.
            query: The query (over parent) defining this view.
        """
        self._parent = parent
        self._query = query

    def _query_string(self) -> Tuple[str, Tuple[Any]]:
        """Returns the SQL query string and values underlying this view."""
        # pylint: disable=protected-access
        return self._query.to_sql_query_string(
            f"\"{self._parent._table_name}\"")

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        rows = []
        try:
            # pylint: disable-next=protected-access
            with self._parent._connection.cursor(
                connector.DictCursor) as cursor:
                cursor.execute(query_string, query_values)
                row_dict = cursor.fetchone()
                while row_dict is not None:
                    # pylint: disable-next=protected-access
                    if self._parent._auto_ddl:
                        row_dict = _clean_row_dict(row_dict)
                    row_dict = _standardize_output(row_dict)
                    rows.append(row_dict)
                    row_dict = cursor.fetchone()
            self._parent._connection.commit()
        except connector.errors.ProgrammingError as error:
            self._parent._connection.rollback()  # pylint: disable=protected-access
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                cursor.execute(
                    f"SELECT COUNT(*) FROM \"{self._parent._table_name}\"")  # pylint: disable=protected-access
                row_count = cursor.fetchone()[0]
            self._parent._connection.commit()  # pylint: disable=protected-access
            if row_count == 0:
                rows = []
            else:
                raise error
        return rows.__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        try:
            # pylint: disable-next=protected-access
            with self._parent._connection.cursor(
                connector.DictCursor) as cursor:
                query_string, query_values = self._query_string()
                cursor.execute(
                    f"SELECT * FROM ({query_string}) AS subquery LIMIT 1",
                    query_values)
                row_dict = cursor.fetchone()
            # pylint: disable-next=protected-access
            self._parent._connection.commit()
        except connector.errors.ProgrammingError as error:
            self._parent._connection.rollback()  # pylint: disable=protected-access
            with self._parent._connection.cursor() as cursor:  # pylint: disable=protected-access
                cursor.execute(
                    f"SELECT COUNT(*) FROM \"{self._parent._table_name}\"")  # pylint: disable=protected-access
                row_count = cursor.fetchone()[0]
            self._parent._connection.commit()  # pylint: disable=protected-access
            if row_count == 0:
                return None
            raise error
        if row_dict is not None:
            # pylint: disable-next=protected-access
            if self._parent._auto_ddl:
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


class SnowflakeTable(table.SqlQueryable, table.Appendable):
    """A Table backed by a Snowflake table."""

    def __init__(
        self,
        user: str,
        password: str,
        account: str,
        database: str,
        schema: str,
        warehouse: str,
        table_name: str,
        auto_ddl: bool = True):
        """Constructs a new SnowflakeTable instance.

        Args:
            user: Snowflake username.
            password: Password for user.
            account: Snowflake account name.
            database: Name of database containing table.
            schema: Name of schema containing table.
            warehouse: Name of warehouse to use for queries.
            table_name: Name of table in database given by preceding arguments.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """

        self._connection_params = {
            "user": user,
            "password": password,
            "account": account,
            "autocommit": False
        }
        self._table_name = table_name
        self._database = database
        self._schema = schema
        self._warehouse = warehouse
        self._auto_ddl = auto_ddl

        self._connection = connector.connect(
            **self._connection_params)
        with self._connection.cursor() as cursor:
            cursor.execute(f"USE WAREHOUSE {warehouse}")
            cursor.execute(f"USE DATABASE {database}")
            cursor.execute(f"USE SCHEMA {schema}")
            if self._auto_ddl:
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS \"{self._table_name}\" "
                    f"(\"{_PLACEHOLDER_COLUMN}\" INTEGER)")
        self._connection.commit()

    def __del__(self):
        """Closes self._connection as necessary on object destruction."""
        if ("sys" in globals() and hasattr("sys", "modules")):
            # To ensure that the Python interpreter is not currently exiting
            # (self._connection.close() here may raise an exception if called
            # while interpreter is exiting).
            self._connection.close()

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        return SnowflakeView(self, table.SqlSelectQuery("*")).__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        return SnowflakeView(self, table.SqlSelectQuery("*")).first_row()

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        row = self.first_row()
        return list(row.keys()) if row is not None else []

    def pandas_df(self) -> pd.DataFrame:
        """See base class."""
        with self._connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM \"{self._table_name}\"")
            df = cursor.fetch_pandas_all()
        self._connection.commit()
        return df

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        metadata = self._connection_params.copy()
        del metadata["autocommit"]
        del metadata["password"]
        metadata["table_name"] = self._table_name
        metadata["database"] = self._database
        metadata["schema"] = self._schema
        metadata["warehouse"] = self._warehouse
        metadata["auto_ddl"] = self._auto_ddl
        return metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "SnowflakeTable":
        """See base class."""
        return SnowflakeTable(**_format_metadata(metadata))

    def indexed_columns(self) -> Iterable[str]:
        """See base class."""
        return []

    def select(self, expression: str, after_from: str = "") -> SnowflakeView:
        """See base class."""
        return SnowflakeView(
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
        with self._connection.cursor(
            connector.DictCursor) as cursor:
            cursor.execute(f"SELECT * FROM \"{self._table_name}\" LIMIT 0")
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
                                f"ALTER TABLE \"{self._table_name}\" "
                                f"ADD COLUMN \"{col_name}\" "
                                f"TEXT DEFAULT NULL")
                            cursor.execute(
                                f"ALTER TABLE \"{self._table_name}\" "
                                f"ADD COLUMN \"{col_name_all_null}\" "
                                f"TEXT DEFAULT NULL")
                        existing_col_names.add(col_name)
                        existing_col_names.add(col_name_all_null)
                    else:
                        if isinstance(value, bool):
                            snowflake_type = "BOOLEAN"
                        elif isinstance(value, int):
                            snowflake_type = "INTEGER"
                        elif isinstance(value, float):
                            snowflake_type = "DOUBLE PRECISION"
                        elif isinstance(value, str):
                            snowflake_type = "TEXT"
                        elif isinstance(value, bytes):
                            snowflake_type = "BINARY"
                        elif isinstance(value, datetime.datetime):
                            snowflake_type = "TIMESTAMP_NTZ"
                        elif isinstance(value, datetime.date):
                            snowflake_type = "DATE"
                        else:
                            raise TypeError(
                                f"Unsupported value type: {type(value)}")
                        with self._connection.cursor() as cursor:
                            if col_name in existing_col_names:
                                cursor.execute(
                                    f"ALTER TABLE \"{self._table_name}\" "
                                    f"DROP COLUMN \""
                                    f"{col_name + _ALL_NULL_COLUMN_SUFFIX}"
                                    f"\"")
                                existing_col_names.remove(
                                    col_name + _ALL_NULL_COLUMN_SUFFIX)
                                cursor.execute(
                                    f"ALTER TABLE \"{self._table_name}\" "
                                    f"DROP COLUMN \"{col_name}\"")
                                cursor.execute(
                                    f"ALTER TABLE \"{self._table_name}\" "
                                    f"ADD COLUMN \"{col_name}\" "
                                    f"{snowflake_type} DEFAULT NULL")
                            else:
                                cursor.execute(
                                    f"ALTER TABLE \"{self._table_name}\" "
                                    f"ADD COLUMN \"{col_name}\" "
                                    f"{snowflake_type}")
                                existing_col_names.add(col_name)
                                if (col_name + _ALL_NULL_COLUMN_SUFFIX in
                                    existing_col_names):
                                    cursor.execute(
                                        f"ALTER TABLE \"{self._table_name}\" "
                                        f"DROP COLUMN "
                                        f"\""
                                        f"{col_name + _ALL_NULL_COLUMN_SUFFIX}"
                                        f"\"")
                                    existing_col_names.remove(
                                        col_name + _ALL_NULL_COLUMN_SUFFIX)
                        self._connection.commit()

    def extend(self, rows: Iterable[table.Row]):
        """See base class."""
        self._add_table_columns(rows)
        with self._connection.cursor() as cursor:
            for row in rows:
                all_values_none = all(value is None for value in row.values())
                if all_values_none:
                    cursor.execute(f"SHOW COLUMNS IN \"{self._table_name}\"")
                    col_list = cursor.fetchall()
                    default_values = ",".join(["DEFAULT" for _ in col_list])
                    cursor.execute(
                        f"INSERT INTO \"{self._table_name}\" "
                        f"VALUES ({default_values})")
                else:
                    col_names = [k for k, v in row.items() if v is not None]
                    col_names_clause = ",".join([f"\"{c}\"" for c in col_names])
                    values_clause = ",".join(["%s" for _ in col_names])
                    cursor.execute(
                        f"INSERT INTO \"{self._table_name}\" "
                        f"({col_names_clause}) "
                        f"VALUES({values_clause})",
                        tuple(row[c] for c in col_names))
        self._connection.commit()

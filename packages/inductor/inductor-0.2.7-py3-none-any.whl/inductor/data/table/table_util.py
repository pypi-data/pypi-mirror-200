"""Utility functions for working with Inductor Tables."""

import re
from typing import Iterable, Optional, Tuple

from inductor.data.table import mysql
from inductor.data.table import postgresql
from inductor.data.table import sqlite
from inductor.data.table import table

def parse_database_url(
    database_url: str) -> Tuple[str, str, str, str, Optional[int], str]:
    """Parses a database URL and returns its fields.

    Args:
        database_url: The database URL to be parsed, in the format
            system://username:password@host:port/database where system is
            mysql, postgresql, or postgres.

    Returns:
        A tuple containing (system, username, password, host, port if present,
        database).

    Raises:
        ValueError if database_url is not properly formatted.
    """
    pattern = (
        r"\A(mysql|postgresql|postgres)://([^:]+?):([^@]+?)@([^/]+?)/(.+)\Z")
    match = re.search(pattern, database_url)
    if match is None:
        raise ValueError(
            f"database_url ({database_url}) does not have the "
            f"expected format.")
    system, username, password, host_port, database = match.groups()
    if ":" in host_port:
        parts = host_port.split(":")
        if len(parts) == 1:
            host, port = host_port, None
        elif len(parts) == 2:
            host, port = parts
            port = int(port)
        else:
            raise ValueError(
                f"database_url ({database_url}) does not have the "
                f"expected format.")
    return system, username, password, host, port, database


def table_from_url(
    database_url: str,
    table_name: str,
    primary_key_column: Optional[str] = None,
    indexed_columns: Iterable[str] = tuple()) -> table.Table:
    """Returns a new table instance based on given arguments.

    If the returned table type takes an auto_ddl parameter, it will be set
    to True.

    Args:
        database_url: URL identifying a database, in either of the following
            formats:
                (a) system://username:password@host:port/database
                    where system is mysql, postgresql, or postgres.
                (b) sqlite://filepath
        table_name: Table name within database given by database_url.
        primary_key_column: Optionally, name of column containing primary key.
        indexed_columns: Names of columns that should be indexed for faster
            queries.
    """
    # SQLite
    if database_url.startswith("sqlite://"):
        filepath = database_url[len("sqlite://"):]
        if primary_key_column is None:
            return sqlite.SqliteTable(
                db_file_path=filepath,
                table_name=table_name,
                indexed_columns=indexed_columns,
                auto_ddl=True)
        else:
            return sqlite.SqliteKeyedTable(
                db_file_path=filepath,
                table_name=table_name,
                primary_key_column=primary_key_column,
                indexed_columns=indexed_columns,
                auto_ddl=True)
    # MySQL or PostgreSQL
    system, username, password, host, port, database = parse_database_url(
        database_url)
    if system == "mysql":
        if primary_key_column is None:
            return mysql.MysqlTable(
                host=host,
                user=username,
                password=password,
                database=database,
                table_name=table_name,
                indexed_columns=indexed_columns,
                port=port,
                auto_ddl=True)
        else:
            return mysql.MysqlKeyedTable(
                host=host,
                user=username,
                password=password,
                database=database,
                table_name=table_name,
                primary_key_column=primary_key_column,
                indexed_columns=indexed_columns,
                port=port,
                auto_ddl=True)
    elif system in ("postgresql", "postgres"):
        if primary_key_column is None:
            return postgresql.PostgresqlTable(
                host=host,
                user=username,
                password=password,
                database=database,
                table_name=table_name,
                indexed_columns=indexed_columns,
                port=port,
                auto_ddl=True)
        else:
            return postgresql.PostgresqlKeyedTable(
                host=host,
                user=username,
                password=password,
                database=database,
                table_name=table_name,
                primary_key_column=primary_key_column,
                indexed_columns=indexed_columns,
                port=port,
                auto_ddl=True)
    else:
        raise ValueError(f"Unrecognized system: {system}")

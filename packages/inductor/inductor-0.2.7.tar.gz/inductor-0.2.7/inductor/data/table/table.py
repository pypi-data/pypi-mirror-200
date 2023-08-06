# Copyright 2022 Inductor, Inc.

"""Abstractions over table-structured storage systems.

For example, table-structured storage systems include relational databases, data
warehouses, data lakes, data lakehouses, and document stores.
"""

import abc
import string
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import pandas as pd


# Type for rows in a Table.
Row = Dict[str, Any]


def _interpolate_sql(
    raw_str: str,
    placeholder: str) -> Tuple[str, Tuple[Any]]:
    """Returns SQL string interpolated.

    If raw_str contains segments enclosed in curly braces, interpolates the
    given string using the values of the variables in the stack frame, three
    frames above (via string.Formatter).

    Args:
        raw_str: Raw string to interpolate.
        placeholder: Placeholder to fill the curly braces from raw string.

    Returns:
        A tuple containing (raw_str with curly-braced segments replaced by
        placeholder, Python values of expressions contained in curly-braced
        segments of raw_str evaluated using variable values in stack frame three
        frames above).
    """
    conversions = {"a": ascii, "r": repr, "s": str}
    previous_frame = sys._getframe(3) # pylint: disable=protected-access
    result = []
    values = []
    parts = string.Formatter().parse(raw_str)
    for part in parts:
        literal_text, field_name, format_spec, conversion = part
        if literal_text:
            result.append(literal_text)
        if not field_name:
            continue
        value = eval(  # pylint: disable=eval-used
            field_name,
            previous_frame.f_globals,
            previous_frame.f_locals)
        if conversion:
            value = conversions[conversion](value)
        if format_spec:
            value = format(value, format_spec)
        if isinstance(value, (list, tuple, set)):
            result.append(",".join([placeholder] * len(value)))
            for v in value:
                values.append(v)
        else:
            result.append(placeholder)
            values.append(value)
    return ("".join(result), tuple(values))


class SqlSelectQuery:
    """Container for specification of a SQL SELECT query over a table."""

    def __init__(
        self,
        expression: str,
        after_from: str = "",
        placeholder: str = ""):
        """Initializes a SqlSelectQuery instance.

        Interpolates expression or after_from if either contains segments
        enclosed in curly braces; the interpolation is done using the values of
        the variables in the stack frame two frames above. The semantics of the
        interpolation are those of Python's built-in `str.format()`.

        Args:
            expression: SQL clause that will appear between SELECT and FROM.
            after_from: SQL clause that will appear after FROM clause.
            placeholder: Placeholder that will replace curly-braced segments in
                `expression` and `after_from` (generally should be placeholder
                required by the data system's Python connector library).
        """
        self.expression, self.expression_values = _interpolate_sql(
            expression, placeholder)
        self.after_from, self.after_from_values = _interpolate_sql(
            after_from, placeholder)

    def to_sql_query_string(self, from_string: str) -> Tuple[str, Tuple[Any]]:
        """Returns SQL SELECT query string and values implied by this instance.

        Args:
            from_string: String to be used in the query's FROM clause.
        """
        return (f"SELECT {self.expression} FROM {from_string} "
                f"{self.after_from}",
                self.expression_values + self.after_from_values)


class Table(abc.ABC):
    """A set of Rows, backed by structured storage.

    All tables must allow scans.  Subclasses may provide additional modes of
    access (e.g., fast range queries, general SQL SELECT queries) and/or the
    ability to write to tables (e.g., by appending rows, by associating a row
    with a primary key).
    """

    @abc.abstractmethod
    def __iter__(self) -> Iterable[Row]:
        """Returns an iterable over this table's rows."""

    @abc.abstractmethod
    def first_row(self) -> Optional[Row]:
        """Returns first row in this table, or None if table is empty."""

    @property
    @abc.abstractmethod
    def columns(self) -> Optional[Iterable[str]]:
        """Returns this table's columns' names, if efficiently retrievable.

        Returns:
            The names of this table's columns, if efficiently retrievable from
            the underlying storage system (e.g., without iterating over
            all rows in the table); otherwise, returns None.
        """

    def column_values(self) -> Dict[str, List[Any]]:
        """Returns a Dict mapping column names to lists of column values."""
        names_to_values = {}
        for row in self:
            if not names_to_values:
                names_to_values = {k: [] for k in row.keys()}
            assert len(row) == len(names_to_values)
            for k, v in row.items():
                names_to_values[k].append(v)
        return names_to_values

    def pandas_df(self) -> pd.DataFrame:
        """Returns a Pandas DataFrame containing this table's data."""
        return pd.DataFrame(self)

    def values(self) -> List[Any]:
        """Returns a list containing the single value stored in each row.

        Requires that this table contains exactly one column.

        Raises:
            RuntimeError if this table does not contain exactly one column.
        """
        values = []
        column_name = None
        for row in self:
            if len(row) != 1:
                raise RuntimeError(
                    "This table does not contain exactly one column.")
            cur_column_name = next(iter(row.keys()))
            if column_name is None:
                column_name = cur_column_name
            elif column_name != cur_column_name:
                raise RuntimeError(
                    "Encountered multiple different column names.")
            values.append(row[column_name])
        return values

    def value(self) -> Any:
        """Returns the single value stored in this table.

        Requires that this table contains exactly one value.

        Raises:
            RuntimeError if table does not contain exactly one row and one
            column.
        """
        v = None
        valid_data = False
        for row in self:
            if not valid_data:
                if len(row) == 1:
                    v = list(row.values())[0]
                    valid_data = True
                else:
                    break
            else:
                valid_data = False
                break
        if valid_data:
            return v
        else:
            raise RuntimeError(
                "Table does not contain exactly one row and one column.")

    @abc.abstractmethod
    def to_metadata(self) -> Dict[str, Any]:
        """Returns metadata sufficient to reconstitute this object.

        The returned value must be JSON-serializable by json.dumps().
        """

    @staticmethod
    @abc.abstractmethod
    def from_metadata(metadata: Dict[str, Any]) -> "Table":
        """Returns Table object represented by metadata.

        Args:
            metadata: Metadata representing a Table of a specific concrete
                subclass type, as produced by that subclass type's
                to_metadata() method.

        Raises:
            ValueError if metadata was not produced by the to_metadata()
            method of an instance of the class implementing this function.
        """


class SqlQueryable(Table):
    """A table that provides SQL SELECT queries."""

    @abc.abstractmethod
    def indexed_columns(self) -> Iterable[str]:
        """Returns names of columns indexed for fast queries."""

    @abc.abstractmethod
    def select(self, expression: str, after_from: str = "") -> Table:
        """Returns result of executing a SQL SELECT query on this table.

        In particular, returns the result of executing the query "SELECT
        {expression} FROM {this view} {after_from}".

        Any curly-brace-enclosed segments within expression and
        after_from are interpolated with the values resulting from
        evaluating the curly-braced segments. Lists, tuples, and sets
        are interpolated as comma-separated lists of values.

        Args:
            expression: SQL clause that will appear between SELECT and FROM.
            after_from: SQL clause that will appear after FROM clause.

        Returns:
            Table giving result set for query.
        """

    def __len__(self) -> int:
        """Returns number of rows in this table."""
        return self.select("count(*) as \"c\"").first_row()["c"]

    def shape(self) -> Tuple[int, int]:
        """Returns (number of rows, number of columns) in this table."""
        row = self.first_row()
        return (len(self), len(row) if row else 0)


class PrimaryKeyQueryable(Table):
    """A table that provides fast queries by unique primary key."""

    @abc.abstractmethod
    def primary_key_column(self) -> str:
        """Returns name of column containing primary key."""

    @abc.abstractmethod
    def get(self, key: Any, default: Optional[Row] = None) -> Optional[Row]:
        """Returns row having given primary key.

        Args:
            key: Primary key value.
            default: Value returned if no row having given primary key exists.

        Returns:
            Row having given primary key if such a row exists; otherwise,
            returns default.
        """

    def __getitem__(self, key: Any) -> Row:
        """Returns row having given primary key.

        Args:
            key: Primary key value.

        Raises:
            KeyError if no row exists having given primary key.
        """
        row = self.get(key)
        if row is not None:
            return row
        else:
            raise KeyError("No row exists for given key.")

    @abc.abstractmethod
    def __contains__(self, key: Any) -> bool:
        """Returns True if table contains given primary key, False otherwise.

        Args:
            key: Primary key value.
        """


class Appendable(Table):
    """A table to which rows can be appended."""

    @abc.abstractmethod
    def extend(self, rows: Iterable[Row]):
        """Adds given rows to this table.

        Args:
            rows: Rows to be added to this table.
        """

    def append(self, row: Row):
        """Adds given row to this table.

        Args:
            row: Row to be added to this table.
        """
        self.extend([row])


class PrimaryKeyWritable(Appendable):
    """A table providing fast row insert, update, and delete by primary key."""

    @abc.abstractmethod
    def primary_key_column(self) -> str:
        """Returns name of column containing primary key."""

    @abc.abstractmethod
    def set(self, key: Any, row: Row, skip_if_exists: bool = False) -> bool:
        """Replaces row having given primary key with given row values.

        If no row currently exists having given primary key, then a new row is
        inserted having that primary key and given row values.  Otherwise, if
        skip_if_exists is False, the existing row is replaced with the given
        row values.

        Args:
            key: Primary key value.
            row: Row values.
            skip_if_exists: If True, then this method does nothing if a row
                having the given primary key value is already present in this
                table.

        Returns:
            True if row was inserted or replaced, and False otherwise.
        """

    def __setitem__(self, key: Any, row: Row):
        """Replaces row having given primary key with given row values.

        If no row currently exists having given primary key, then a new row is
        inserted having that primary key and given row values.  Otherwise, the
        existing row is replaced with the given row values.

        Alias for set(key, row, skip_if_exists=False).

        Args:
            key: Primary key value.
            row: Row values.
        """
        self.set(key, row, skip_if_exists=False)

    @abc.abstractmethod
    def update(self, key: Any, values: Row):
        """Updates row having given primary key to contain given values.

        If no row currently exists having given primary key, then a new row is
        inserted having that primary key and the given values.  Otherwise, the
        existing row is updated to have the given values; only columns
        explicitly referenced in values are updated.

        Args:
            key: Primary key value.
            values: Values to assign to a subset of columns.
        """

    @abc.abstractmethod
    def __delitem__(self, key: Any):
        """Deletes row having given primary key.

        Nothing occurs if no row exists having given primary key.

        Args:
            key: Primary key value.
        """

    @abc.abstractmethod
    def increment(
        self,
        key: Any,
        column_name: str,
        increment_by: int) -> Union[int, float]:
        """Increments specified column in row having given primary key.

        The increment is performed atomically.

        Args:
            key: Primary key value.
            column_name: Name of column to be incremented.
            increment_by: Value by which to increment.

        Returns:
            The new value of the column after it has been incremented.
        """


class WithPrimaryKey(PrimaryKeyQueryable, PrimaryKeyWritable):
    """Type for tables that are PrimaryKeyQueryable and PrimaryKeyWritable."""

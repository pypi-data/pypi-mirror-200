# Copyright 2022 Inductor, Inc.

"""Abstractions for DynamoDB tables."""

import datetime
import decimal
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import boto3
from botocore import exceptions

from inductor.data.table import table


# Supported Python types for primary key columns in this implementation.
PrimaryKeyColumnType = Union[str, int, decimal.Decimal, bytes]
# Supported types for keys passed to this module's public
# methods as parameters.
PrimaryKeyType = Union[
    PrimaryKeyColumnType,
    Tuple[PrimaryKeyColumnType, PrimaryKeyColumnType],
    List[PrimaryKeyColumnType]
]


def _standardize_input(value: Any) -> Any:
    """Converts a value to be able to be stored in DynamoDB.

    DynamoDB does not support all Python data types. This method converts
    values to a data type that is compatible with being
    inserted into DynamoDB, if possible. This method is the reverse
    of _standardize_output().

    This method adds support for inserting the following data
    types into DynamoDB:
        - float
        - datetime.date
        - datetime.datetime

    Args:
        value: The value to standardize.

    Returns:
        The standardized value.
    """
    if isinstance(value, float):
        return decimal.Decimal(str(value))
    elif isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    elif isinstance(value, dict):
        return {k: _standardize_input(v)
                for k, v in value.items()}
    elif isinstance(value, set):
        return set(_standardize_input(item) for item in value)
    elif isinstance(value, list):
        return [_standardize_input(v) for v in value]
    else:
        return value


def _standardize_output(value: Any) -> Any:
    """Converts values from DynamoDB to their original Python data types.

    DynamoDB does not support all Python data types. This method converts
    values to their original Python data types. This method is based on
    the reverse of _standardize_input().

    This method adds support for getting the following data
    types from DynamoDB:
        - float
        - datetime.date
        - datetime.datetime

    Args:
        value: The value to standardize.

    Returns:
        The standardized value.
    """
    if isinstance(value, decimal.Decimal):
        converted_value = str(value)
        if "." in converted_value:
            return float(converted_value)
        else:
            return int(converted_value)
    elif isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value)
        except ValueError:
            pass
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError:
            pass
        return value
    elif isinstance(value, boto3.dynamodb.types.Binary):
        return value.value
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


class DynamoDBTable(table.WithPrimaryKey):
    """A Table backed by a DynamoDB table."""

    def __init__(
        self,
        table_name: str,
        partition_key_column: str,
        sort_key_column: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        endpoint_url: Optional[str] = None,
    ):
        """Constructs a new DynamoDBTable instance.

        Args:
            table_name: Name of DynamoDB table.
            partition_key_column: Name of column containing partition key
                (i.e., name of DynamoDB partition key attribute). Values
                in the partition key column must be of type str, int, or bytes.
            sort_key_column: Optional name of column containing sort key
                (i.e., name of DynamoDB sort key attribute). Values in the
                sort key column must be of type str, int, or bytes.
            tags: Optional AWS resource tags to be applied when creating
                the table, if the table does not already exist.
            endpoint_url: Optional Endpoint URL to be used to communicate
                with the DynamoDB service.  Intended to be used to connect
                with a local DynamoDB instance for development and testing
                purposes.  In general, should not be provided if utilizing
                an actual AWS account.
        """
        self._table_name = table_name
        self._partition_key_column = partition_key_column
        self._sort_key_column = sort_key_column
        self._tags = tags
        self._endpoint_url = endpoint_url

        self._boto_dyn_resource = boto3.resource(
            "dynamodb", endpoint_url=self._endpoint_url
        )

        # Load the DynamoDB table.
        # If it does not exist, do not create the table until the start of the
        #     first method that adds an item to the table. This is to avoid
        #     creating a table with the incorrect key schema.
        self._load_boto_dyn_table()

    def _table_exists(self) -> bool:
        """Checks if the DynamoDB table exists.

        If the table has not been loaded, attempts to load the table.

        Returns:
            True if the table exists, False otherwise.
        """
        return self._boto_dyn_table is not None or self._load_boto_dyn_table()

    def _load_boto_dyn_table(self) -> bool:
        """Loads the DynamoDB table if it exists.

        Sets self._boto_dyn_table to the Boto3 DynamoDB Table
        Resource if it exists, otherwise sets it to None.
        If the table exists, checks that the columns match
        the primary key.

        Returns:
            True if the table exists, False otherwise.

        Raises:
            ValueError: If the table exists but the primary key does not match.
        """
        try:
            t = self._boto_dyn_resource.Table(self._table_name)
            t.load()
        except exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "ResourceNotFoundException":
                self._boto_dyn_table = None
                return False
            else:
                raise error

        self._boto_dyn_table = t

        # Check that the columns match the primary key columns.
        boto_dyn_partition_key_column = None
        boto_dyn_sort_key_column = None
        for key_schema in self._boto_dyn_table.key_schema:
            if key_schema["KeyType"] == "HASH":
                boto_dyn_partition_key_column = key_schema["AttributeName"]
            elif key_schema["KeyType"] == "RANGE":
                boto_dyn_sort_key_column = key_schema["AttributeName"]

        if self._partition_key_column != boto_dyn_partition_key_column:
            raise ValueError(
                f"Partition key column mismatch. "
                f"Expected {self._partition_key_column} "
                f"found {boto_dyn_partition_key_column}."
            )
        if self._sort_key_column != boto_dyn_sort_key_column:
            raise ValueError(
                f"Sort key column mismatch. "
                f"Expected {self._sort_key_column} "
                f"found {boto_dyn_sort_key_column}"
            )

        return True

    def _parse_primary_key_value(
        self, key: PrimaryKeyType) -> Dict[str, PrimaryKeyColumnType]:
        """Parses a primary-key-column value and checks that it is valid.

        Args:
            key: The primary-key-column attribute value to check.
                If the table has a sort key, key must be a tuple or list in
                the form (partition_key_column value, sort_key_column value).
                Otherwise key must be in the form of a single
                partition_key_column value. Each partition_key_column value
                or sort_key_column value must be of type str, int,
                decimal.Decimal, or bytes.

        Returns:
            A dictionary containing the following keys:
                partition_key_column:
                    The partition_key_column value.
                sort_key_column (Optional):
                    The sort_key_column value, if it exists.

        Raises:
            ValueError: If the key is not valid.
        """
        if self._sort_key_column is not None:
            if not isinstance(key, (tuple, list)):
                raise ValueError(
                    f"Invalid key type. Expected tuple or list, "
                    f"found {type(key)}."
                )
            if len(key) != 2:
                raise ValueError(
                    f"Invalid key length. Expected 2, found {len(key)}."
                )
            primary_key_value = {
                self._partition_key_column: key[0],
                self._sort_key_column: key[1],
            }
        else:
            primary_key_value = {self._partition_key_column: key}

        for k, v in primary_key_value.items():
            standardized_value = _standardize_input(v)
            primary_key_value[k] = standardized_value
            if not isinstance(standardized_value,
                              (str, int, decimal.Decimal, bytes, float)):
                raise ValueError(
                    f"Primary key column value must be of type str, int, "
                    f"float/decimal.Decimal, or bytes. Found {type(v)}."
                )

        return primary_key_value

    def _validate_row(
        self, primary_key_value: Dict[str, PrimaryKeyColumnType],
        row: table.Row) -> table.Row:
        """Ensures that the given row includes the given primary key.

        If the row does not include the primary key, the primary key is
        added to the row.

        Args:
            primary_key_value: A dictionary containing the primary key
                column values in the form:
                    partition_key_column: The partition_key_column value.
                    sort_key_column (Optional): The sort_key_column value,
                        if it exists.
            row: The row to validate.

        Returns:
            The validated row.

        Raises:
            ValueError: If the row includes a primary key that is
                different from the given primary key.
        """
        for key, value in primary_key_value.items():
            if key not in row:
                row = row.copy()
                row[key] = value
            elif row[key] != value:
                raise ValueError(
                    f"Primary key column {key} mismatch. "
                    f"Expected {value} found {row[key]}."
                )
        return row

    def _create_boto_dyn_table(self, row: table.Row):
        """Creates the DynamoDB table.

        Attempts to create the DynamoDB table using the primary key
        schema implied by the given row. If the table fails to
        be created because it already exists, the table is retrieved
        from DynamoDB. A Boto3 DynamoDB table resource is stored in the
        self._boto_dyn_table attribute.

        Args:
            row: The row to use to create the table. The row is NOT
                inserted into the table.
        """
        def _get_attribute_def(key_column: str, value: Any) -> Dict[str, str]:
            map_type_to_symbol = {str: "S", int: "N",
                                  decimal.Decimal: "N", bytes: "B"}
            return {
                "AttributeName": key_column,
                "AttributeType": map_type_to_symbol[type(value)],
            }

        key_schema = [
            {"AttributeName": self._partition_key_column, "KeyType": "HASH"}]
        attribute_definitions = [
            _get_attribute_def(
                self._partition_key_column, row[self._partition_key_column]
            )
        ]
        if self._sort_key_column is not None:
            key_schema.append(
                {"AttributeName": self._sort_key_column, "KeyType": "RANGE"}
            )
            attribute_definitions.append(
                _get_attribute_def(self._sort_key_column,
                                   row[self._sort_key_column])
            )

        table_config = {
            "TableName": self._table_name,
            "KeySchema": key_schema,
            "AttributeDefinitions": attribute_definitions,
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
        }
        if self._tags is not None:
            table_config["Tags"] = self._tags

        try:
            self._boto_dyn_table = self._boto_dyn_resource.create_table(
                **table_config)
            self._boto_dyn_table.wait_until_exists()
        except exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "ResourceInUseException":
                # The DynamoDB table was created by another process,
                # so load the DynamoDB table resource.
                if not self._load_boto_dyn_table():
                    raise error
            else:
                raise error

    def _parse_scan_page_item(self, type_value: Dict[str, Any]) -> Any:
        """Parses the value returned by DynamoDB's scan paginator.

        Converts the given value to a Python data type based
        on its provided AttributeType. Note that this method
        does not fully convert the value to its original Python
        data type. It only converts the value to the correct
        Python data type for the AttributeType. In order to
        fully convert the value to its original Python data type,
        the value must be passed to _standardize_output(),
        after first passing through this method.

        Args:
            type_value: A single key-value pair to parse in the format:
                {AttributeType: AttributeValue}
                    where AttributeValue is initially
                    not necessarily the same Python data
                    type as denoted by AttributeType.

        Returns:
            The parsed value.
        """
        if len(type_value) != 1:
            raise ValueError(
                f"Expected a single key-value pair, found {type_value}."
            )
        for attr_type, value in type_value.items():
            if attr_type == "N":
                return decimal.Decimal(value)
            elif attr_type == "NULL":
                return None
            elif attr_type in ("SS", "NS", "BS"):
                subtype = attr_type.replace("S", "")
                return set(
                    self._parse_scan_page_item({subtype: v})
                    for v in value)
            elif attr_type == "L":
                return [
                    self._parse_scan_page_item(v)
                    for v in value]
            elif attr_type == "M":
                return {
                    k: self._parse_scan_page_item(v)
                    for k, v in value.items()}
            return value

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        if not self._table_exists():
            return iter([])

        boto_dyn_client = boto3.client(
            "dynamodb", endpoint_url=self._endpoint_url)

        # Scan pagination returns each item's attributes in the format:
        #   {AttributeType: {AttributeName: AttributeValue}}
        #       where AttributeValue is not necessarily the same
        #       Python type as denoted by AttributeType.
        # We need to convert this to the format:
        #   {AttributeName: AttributeValue}
        #       where AttributeValue is the same Python type as
        #       denoted by AttributeType.
        paginator = boto_dyn_client.get_paginator("scan")
        paginator = paginator.paginate(TableName=self._table_name)
        for page in paginator:
            for item in page["Items"]:
                item_dict = {}
                for key, type_value in item.items():
                    item_dict[key] = self._parse_scan_page_item(type_value)
                yield _standardize_output(item_dict)

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        if not self._table_exists():
            return None

        response = self._boto_dyn_table.scan(Limit=1)
        if "Items" in response and len(response["Items"]) > 0:
            return _standardize_output(response["Items"][0])
        else:
            return None

    @property
    def columns(self) -> Optional[Iterable[str]]:
        """See base class."""
        return None

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        metadata = {}
        metadata["table_name"] = self._table_name
        metadata["partition_key_column"] = self._partition_key_column
        metadata["sort_key_column"] = self._sort_key_column
        metadata["tags"] = self._tags
        metadata["endpoint_url"] = self._endpoint_url
        return metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "DynamoDBTable":
        """See base class."""
        return DynamoDBTable(**metadata)

    def extend(self, rows: Iterable[table.Row]):
        """See base class."""
        standardized_rows = []
        for row in rows:
            standardized_rows.append(
                _standardize_input(row))

        if not self._table_exists():
            self._create_boto_dyn_table(standardized_rows[0])

        with self._boto_dyn_table.batch_writer() as batch:
            for row in standardized_rows:
                batch.put_item(Item=row)

    def primary_key_column(self) -> Union[str, Tuple[str, str]]:
        """See base class."""
        if self._sort_key_column is not None:
            return (self._partition_key_column, self._sort_key_column)
        else:
            return self._partition_key_column

    def get(
        self,
        key: Any,
        default: Optional[table.Row] = None) -> Optional[table.Row]:
        """See base class."""
        if not self._table_exists():
            return default

        primary_key_value = self._parse_primary_key_value(key)

        response = self._boto_dyn_table.get_item(Key=primary_key_value)

        if "Item" in response:
            return _standardize_output(response["Item"])
        else:
            return default

    def __contains__(self, key: Any) -> bool:
        """See base class."""
        if not self._table_exists():
            return False

        primary_key_value = self._parse_primary_key_value(key)

        response = self._boto_dyn_table.get_item(
            Key=primary_key_value,
            ProjectionExpression=self._partition_key_column
        )

        return "Item" in response

    def set(
        self,
        key: Any,
        row: table.Row,
        skip_if_exists: bool = False) -> bool:
        """See base class."""
        primary_key_value = self._parse_primary_key_value(key)

        standardized_row = _standardize_input(row)
        standardized_row = self._validate_row(primary_key_value,
                                              standardized_row)

        if not self._table_exists():
            self._create_boto_dyn_table(standardized_row)

        put_item = {
            "Item": standardized_row,
        }

        # To prevent a new item from replacing an existing item, use a
        # conditional expression that contains the attribute_not_exists
        # function with the name of the attribute being used as the
        # partition/sort key for the table. Since every record must contain
        # that attribute, the attribute_not_exists function will only
        # succeed if no matching item exists.
        if skip_if_exists:
            condition_expression = (
                f"attribute_not_exists({self._partition_key_column})")
            if self._sort_key_column is not None:
                condition_expression += (
                    f" AND attribute_not_exists({self._sort_key_column})")
            put_item["ConditionExpression"] = condition_expression

        try:
            self._boto_dyn_table.put_item(**put_item)
            return True
        except exceptions.ClientError as error:
            if error.response["Error"][
                "Code"] == "ConditionalCheckFailedException":
                return False
            else:
                raise error

    def update(self, key: Any, values: table.Row):
        """See base class."""
        primary_key_value = self._parse_primary_key_value(key)

        standardized_row = _standardize_input(values)
        standardized_row = self._validate_row(primary_key_value,
                                              standardized_row)

        if not self._table_exists():
            self._create_boto_dyn_table(standardized_row)

        # It is required that the primary key be excluded
        #   from the row in the update_item call.
        standardized_row = standardized_row.copy()
        del standardized_row[self._partition_key_column]
        if self._sort_key_column is not None:
            del standardized_row[self._sort_key_column]

        # If the row only contains the primary key,
        #   then use the set method instead.
        if len(standardized_row) == 0:
            self.set(key=key, row=values, skip_if_exists=True)
            return

        # ExpressionAttributeNames is required to allow
        #   the use of reserved words as column names.
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        for column, value in standardized_row.items():
            update_expression += f"#{column} = :{column}, "
            expression_attribute_values[f":{column}"] = value
            expression_attribute_names[f"#{column}"] = column
        update_expression = update_expression[:-2]

        self._boto_dyn_table.update_item(
            Key=primary_key_value,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )

    def __delitem__(self, key: Any):
        """See base class."""
        if not self._table_exists():
            return

        primary_key_value = self._parse_primary_key_value(key)

        self._boto_dyn_table.delete_item(Key=primary_key_value)

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
        if column_name in (self._partition_key_column, self._sort_key_column):
            raise ValueError("Cannot increment primary key column.")

        primary_key_value = self._parse_primary_key_value(key)
        try:
            response = self._boto_dyn_table.update_item(
                Key=primary_key_value,
                UpdateExpression=(
                    f"SET #{column_name} = #{column_name} + :increment_by"),
                ExpressionAttributeValues={":increment_by": increment_by},
                ExpressionAttributeNames={f"#{column_name}": column_name},
                ReturnValues="UPDATED_NEW"
            )
        except exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "ValidationException":
                raise ValueError(
                    f"Column {column_name} does not "
                    f"exist in table for given key value.") from error
            else:
                raise error

        value_updated = str(response["Attributes"][column_name])
        if "." in value_updated:
            return float(value_updated)
        else:
            return int(value_updated)

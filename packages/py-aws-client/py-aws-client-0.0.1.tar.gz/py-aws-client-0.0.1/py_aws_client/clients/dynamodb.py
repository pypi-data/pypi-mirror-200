import boto3
from typing import Dict, List


class DynamoDb(object):
    def __init__(self, session: boto3.session.Session = None, region: str = None):
        """
        Creates a client using either the boto3 Session or region.
        param session: required when no region is provided
        param region: required when no session is provided
        """
        if session and region:
            raise EnvironmentError('1 of session or region must be provided')

        if session:
            self.client = session.client(
                service_name='dynamodb',
            )
        elif region:
            self.client = boto3.client(
                service_name='dynamodb',
                region_name=region
            )

    def create_table(self, attribute_definitions: List, table_name: str, key_schema: List,
                     provisioned_throughput: Dict = None) -> Dict[str, any]:
        """
        Create a table in DynamoDB
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
        param attribute_definitions: An array of attributes that describe the key schema for the table and indexes.
        param table_name: The name of the table to create.
        param key_schema: The attributes that make up the primary key for a table or an index.
        param provisioned_throughput: Provisioned read and write capacity for the table.
        """
        if provisioned_throughput is None:
            provisioned_throughput = {
                # ReadCapacityUnits set to 5 strongly consistent reads per second
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  # WriteCapacityUnits set to 5 writes per second
            }

        response = self.client.create_table(
            AttributeDefinitions=attribute_definitions,
            TableName=table_name,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput,
        )

        return response

    def get_item(self, table_name: str, key: Dict[str, any]) -> Dict[str, any]:
        """
        Gets item from table https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
        #DynamoDB.Client.get_item :param table_name: name of the table :param key: a map of attribute names to
        AttributeValue objects, representing the primary key of the item to retrieve.
        """
        response = self.client.get_item(
            TableName=table_name,
            Key=key,
        )

        return response

    def put_item(self, table_name: str, item: Dict[str, any]) -> Dict[str, any]:
        """
        Creates a new item, or replaces an old item with a new item. If an item that has the same primary key as the
        new item already exists in the specified table, the new item completely replaces the existing item.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client
        .put_item :param table_name: name of the table :param item: A map of attribute name/value pairs, one for each
        attribute. Only the primary key attributes are required; you can optionally provide other attribute
        name-value pairs for the item.
        """
        response = self.client.put_item(
            TableName=table_name,
            Item=item,
        )

        return response

    def update_item(self, table_name: str, key: Dict[str, any], attribute_updates: Dict[str, any]) -> Dict[str, any]:
        """
        Edits an existing item's attributes, or adds a new item to the table if it does not already exist.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client
        :param attribute_updates:
        :param table_name: name of the table
        :param key: A map of attribute name/value pairs, one for each attribute. Only the primary key attributes are
        required; you can optionally
        provide other attribute name-value pairs for the item.
        param attribute_updates: a map of attributes to update, must have keys for 'Value' and 'Action'
        """
        response = self.client.update_item(
            TableName=table_name,
            Key=key,
            AttributeUpdates=attribute_updates,
        )

        return response

    def delete_item(self, table_name: str, key: Dict[str, any],
                    expected: Dict[str, Dict[str, bool]] = None) -> Dict[str, any]:
        """
        Deletes a single item in a table by primary key.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client
        :param expected:
        :param table_name: name of the table
        :param key: A map of attribute
        name/value pairs, one for each attribute. Only the primary key attributes are required; you can optionally
        provide other attribute name-value pairs for the item.
        param expected: a map of attributes that are expected
        to be present or not in the table, if it is not an exception will be raised.
        """
        if expected is None:
            expected = {}

        response = self.client.delete_item(
            TableName=table_name,
            Key=key,
            Expected=expected
        )

        return response

    def query_table(self, table_name: str, partition_key_name: str,
                    partition_key_value: Dict[str, Dict[str, any]]) -> Dict[str, any]:
        """
        Queries specified table and returns the item(s). The primary key is required
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query
        :param table_name: Name of the table
        :param partition_key_name: the primary key name of the table
        :param partition_key_value: the value for the primary key
        """
        response = self.client.query(
            TableName=table_name,
            KeyConditionExpression=partition_key_name,
            ExpressionAttributeValues=partition_key_value
        )

        return response

    def scan_table(self, table_name: str) -> Dict[str, any]:
        """
        Returns one or more items and item attributes in a specified table
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan
        :param table_name: name of the table
        """
        response = self.client.scan(
            TableName=table_name,
        )

        return response

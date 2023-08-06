import boto3
from typing import Dict, List, Optional
from botocore.exceptions import ClientError


class SecretsManager(object):
    def __init__(self, session: boto3.session.Session = None, region: str = None):
        """
        Creates a client using either the boto3 Session or region.
        :param session: required when no region is provided
        :param region: required when no session is provided
        """
        if session and region:
            raise EnvironmentError('1 of session or region must be provided')

        if session:
            self.client = session.client(
                service_name='secretsmanager',
            )
        elif region:
            self.client = boto3.client(
                service_name='secretsmanager',
                region_name=region
            )

    def get_secret_value(self, secret_name: str) -> Dict[str,  any]:
        """
        Gets a secret value from Secrets Manager
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html
        :param secret_name: name of the secret stored in Secret Manager
        :return: parameter response dictionary
        """
        response = self.client.get_secret_value(
            SecretId=secret_name,
        )

        return response

    def create_secret(self, secret_name: str, secret_string: str, tags: Optional[List[dict]]=None):
        """
        Creates and stores new secret in AWS secrets manager
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.create_secret
        :param secret_name:
        :param secret_string:
        :param tags:
        :return:
        """
        response = self.client.create_secret(
            Name=secret_name,
            SecretString=secret_string,
            Tags=tags
        )

        return response




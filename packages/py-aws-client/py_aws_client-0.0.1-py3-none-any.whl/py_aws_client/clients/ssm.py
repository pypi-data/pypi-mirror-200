import boto3
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from botocore.exceptions import ClientError


class Ssm(object):
    def __init__(self, session: boto3.session.Session = None, region: str = None):
        """
        Creates a client using either the boto3 Session or region.
        param session: required when no region is provided
        :param region: required when no session is provided
        """
        if session and region:
            raise EnvironmentError('1 of session or region must be provided')

        if session:
            self.client = session.client(
                service_name='ssm',
            )
        elif region:
            self.client = boto3.client(
                service_name='ssm',
                region_name=region
            )

    def get_parameter(self, parameter_name: str, with_decryption: bool = False) -> Dict[str, any]:
        """
        Gets an SSM Parameter
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter
        :param parameter_name: name of the parameter to get from ssm
        :param with_decryption: decrypts the param when true.
        :return: ssm get parameter response
        """
        response = self.client.get_parameter(
            Name=parameter_name,
            WithDecryption=with_decryption
        )
        param_value = response.get('Parameter').get('Value')

        return param_value

    def put_parameter(self, parameter_name: str, parameter_value: str) -> Dict[str, any]:
        """
        Puts an SSM Parameter
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.put_parameter
        :param parameter_name: name of the parameter to get from ssm
        :param parameter_value: decrypts the param when true.
        :return: ssm put parameter response
        """
        response = self.client.put_parameter(
            Name=parameter_name,
            Value=parameter_value,
            Type='SecureString',
            Overwrite=True,
        )

        return response

    def get_command_invocation(self, command_id: str, instance_id: str) -> Dict[str, any]:
        """
        Returns detailed information about command execution for an invocation.

        param command_id: the unique id of the command invocation.
        :param command_id:
        :param instance_id: the unique id of the instance where the command invocation is occurring.
        :return: response: detailed information about command execution for an invocation.
        """
        response = self.client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )

        return response

    def command_waiter(self, command_id: str, instance_id: str) -> Dict[str, any]:
        """
        Attempts to get the status of the given command ID six times and monitors the status until an end state occurs
        such as 'Successful' or 'Failed'.

        param command_id: the unique id of the command invocation.
        :param command_id:
        :param instance_id: the unique id of the instance where the command invocation is occurring.
        :return: response: the response of the SSM get_command_invocation()
        """
        print(f'Attempting to get command status. CommandId: {command_id}')

        start_time = datetime.utcnow()
        while True or (datetime.utcnow() - start_time) < timedelta(hours=2):
            response = None
            status = None
            status_message = None

            try:
                response = self.get_command_invocation(
                    command_id=command_id,
                    instance_id=instance_id
                )
                status = response.get('Status')
                status_message = f'Command ID: {command_id} | Status: {status}'
                print(status_message)

            except ClientError as e:
                if 'InvocationDoesNotExist' == e.response.get('Error').get('Code'):
                    time.sleep(5)
                    continue

            if status == 'Success':
                return response

            elif status in ['Pending', 'InProgress', 'Cancelling']:
                time.sleep(10)

            elif status in ['Cancelled', 'Failed', 'TimedOut']:
                raise EnvironmentError(status_message)

            else:
                raise EnvironmentError(f'Unknown Status encountered.\nStatus: {status}')

    def send_command(self, document_name: str, instance_ids: List[str],
                     parameters=None,
                     document_version: Optional[str] = '$LATEST', wait: Optional[bool] = True,
                     timeout_second: Optional[int] = 2700) -> Dict[str, any]:
        """
        Runs SSM document commands on an EC2 instance.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command
        param timeout_second:
        param document_name: the unique name of the SSM document, which contains the commands to run.
        param document_version: The SSM document version to use in the request.
        param instance_ids: the unique IDs of the instances where the command invocation will occur.
        param parameters: input parameters to the SSM document.
        param wait: defaults to True. If True, waits for the command to reach an end state.
        return response: the SSM send_command() response
        """
        if parameters is None:
            parameters = {}
        response = self.client.send_command(
            DocumentName=document_name,
            DocumentVersion=document_version,
            InstanceIds=instance_ids,
            Parameters=parameters,
            TimeoutSeconds=timeout_second
        )

        command_id = response.get('Command').get('CommandId')

        if wait:
            for instance_id in instance_ids:
                response = self.command_waiter(
                    command_id=command_id,
                    instance_id=instance_id
                )

        return response

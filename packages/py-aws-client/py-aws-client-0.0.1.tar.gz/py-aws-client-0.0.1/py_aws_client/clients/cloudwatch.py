import boto3
from enum import Enum
from typing import List, Dict
from datetime import datetime
from botocore.exceptions import WaiterError


class Cloudwatch(object):
    class Stats(Enum):
        Minimum = 'Minimum'
        Maximum = 'Maximum'
        Average = 'Average'

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
                service_name='cloudwatch',
            )
        elif region:
            self.client = boto3.client(
                service_name='cloudwatch',
                region_name=region
            )

    def get_metric_data(self, namespace: str, instance_id: str, metric: str,
                        stat: Stats, start_time: datetime, end_time: datetime) -> Dict[str, any]:
        """
        Gets metric data for the specified ec2 instance and metric
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data
        :param namespace: Cloudwatch Metrics Namespace to get metric data from
        :param instance_id: the id of the ec2 instance to get metric data for
        :param metric: the name of the metric to get data for
        :param stat: src.bll.aws.Cloudwatch.Stats
        :param start_time: start getting data here
        :param end_time: stop getting data here
        :return: cloudwatch client get metric data response dict
        """
        response = self.client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'instance_query',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric,
                            'Dimensions': [
                                {
                                    'Name': 'InstanceId',
                                    'Value': instance_id
                                },
                            ]
                        },
                        'Period': 7200,
                        'Stat': stat.value,
                    },
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            ScanBy='TimestampDescending',
        )

        return response

    def put_metric_data(self, namespace: str, metric_name: str, value: str, unit: str) -> Dict[str, any]:
        """
        Puts/Updates the metric_name in to the namespace.

        For available units, visit the documentation.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data
        :param namespace: the cloudwatch namespace to associate the metric name
        :param metric_name: name of the metric to create/update
        :param value: the value for the metric
        :param unit: the unit of the metric
        :return: put metric data response
        """
        response = self.client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Timestamp': datetime.now(),
                    'Value': value,
                    'Unit': unit,
                },
            ]
        )

        return response

    def describe_alarms(self, alarm_prefix=None, alarm_names=None, state_value=None) -> Dict:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.describe_alarms
        Get cloudwatch alarms with the optional parameters listed below to filter the alarms.
        Since the max number of alarms the API will return is 99, Next Token allows us to make additional
        requests until we have all the alarms.
        param alarm_prefix: alarm prefix
        param alarm_names: a list of alarm names - has a maximum number of 100
        param state_value: filter for the state of the alarms (OK, ALARM)
        return: cloudwatch describe alarms response
        """
        if alarm_names is None:
            alarm_names = []
        kwargs = dict()

        kwargs["MaxRecords"] = 99
        if state_value:
            kwargs["StateValue"] = state_value
        if alarm_names:
            kwargs["AlarmNames"] = alarm_names
        if alarm_prefix:
            kwargs["AlarmNamePrefix"] = alarm_prefix

        response = self.client.describe_alarms(**kwargs)
        next_token = response.get('NextToken')
        alarms_object = response.get("MetricAlarms", [])
        while next_token:
            kwargs["NextToken"] = next_token
            response = self.client.describe_alarms(**kwargs)
            next_token = response.get('NextToken')
            alarms_object += response.get("MetricAlarms", [])

        return alarms_object

    def disable_alarms(self, alarm_name_list: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.disable_alarm_actions
        :param alarm_name_list: a list of alarms - cannot be larger than 100, so we split it up
        """
        list_of_lists = [alarm_name_list[x:x + 99] for x in range(0, len(alarm_name_list), 99)]

        disabled_alarms = {}
        for sub_list in list_of_lists:
            disabled_alarms = self.client.disable_alarm_actions(
                AlarmNames=sub_list
            )
        return disabled_alarms

    def enable_alarms(self, alarm_name_list: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.enable_alarm_actions
        :param alarm_name_list: a list of alarm names to enable - cannot be larger than 100, so we split it up
        """
        list_of_lists = [alarm_name_list[x:x + 99] for x in range(0, len(alarm_name_list), 99)]
        enabled_alarms = {}
        for sub_list in list_of_lists:
            enabled_alarms = self.client.enable_alarm_actions(
                AlarmNames=sub_list
            )
        return enabled_alarms

    def wait_until_alarm_state(self, alarms_list: List[str], alarm_state: str, wait_in_seconds: int,
                               alarm_type: str = "MetricAlarm") -> bool:
        f"""
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Waiter.AlarmExists.wait
        Waits up to {wait_in_seconds} seconds for alarms to reach {alarm_state} state 
        :param alarms_list: a list of alarm names - maximum number of 100, so we split it up
        :param alarm_type: The type of alarm - defaults to MetricAlarm
        :param alarm_state: the desired state of the alarm we are waiting to achieve
        :param wait_in_seconds: the duration in seconds to wait for the alarm to achieve desired state
        :return: True if alarms reached desired state, False if they did not
        """
        waiter = self.client.get_waiter('alarm_exists')
        list_of_lists = [alarms_list[x:x + 99] for x in range(0, len(alarms_list), 99)]
        try:
            for sub_list in list_of_lists:
                waiter.wait(
                    AlarmNames=sub_list,
                    AlarmTypes=[
                        alarm_type,
                    ],
                    StateValue=alarm_state,
                    WaiterConfig={
                        'Delay': 30,
                        'MaxAttempts': wait_in_seconds / 30
                    }
                )
            print("Alarms reached desired state.")
            return True
        except WaiterError as e:
            print(f"{e}: Alarms did not reach desired state within {wait_in_seconds} seconds.")
            return False

import boto3
from typing import List, Dict
from botocore.exceptions import ClientError


class Elbv2(object):
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
                service_name='elbv2',
            )
        elif region:
            self.client = boto3.client(
                service_name='elbv2',
                region_name=region
            )

    def describe_target_groups(self, target_group_names: List[str]) -> Dict[str, any]:
        """
        Describes the specified target groups

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_groups
        :param target_group_names: The names of the target groups (list)
        :return: aws describe_target_groups response.
        """
        print(f'Describing Target Groups for: {", ".join(target_group_names)}')

        response = self.client.describe_target_groups(
            Names=target_group_names
        )

        return response

    def describe_target_health(self, target_group_arns: List[str]) -> Dict[str, any]:
        """
        Describes the health of the specified targets

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_health
        :param target_group_arns: The Amazon Resource Name (ARN) of the target group
        :return: aws describe_health_target response
        """
        print(f'Describing Target Groups health for: {", ".join(target_group_arns)}')
        response = self.client.describe_target_health(
            TargetGroupArn=target_group_arns
        )

        return response

    def get_target_groups_arns(self, target_group_names: List[str]) -> List:
        """
        Describes the specified target groups and returns the target group ARN

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_groups
        :param target_group_names: The names of the target groups (list)
        :return: target group arns: The Amazon Resource Names (ARN) of the target groups.
        """
        try:
            print(f'Getting Target Groups ARN for: {", ".join(target_group_names)}')

            response = self.client.describe_target_groups(
                Names=target_group_names
            )

            target_group_arns = []
            for target in response['TargetGroups']:
                arn = target['TargetGroupArn']
                target_group_arns.append(arn)
            return target_group_arns
        except ClientError as error:
            raise EnvironmentError(error)

    def get_healthy_instances(self, target_group_arns: List[str]) -> List[str]:
        """
        Gets the healthy instances of the specified target group(s)

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_health
        :param target_group_arns: The Amazon Resource Name (ARN) of the target group
        :return: instance_ids: A list of healthy instances of the target group
        """
        try:
            print(f'Getting healthy instance ids for: {", ".join(target_group_arns)}')

            response = self.client.describe_target_health(
                TargetGroupArn=target_group_arns
            )

            instance_ids = []
            for instance in response['TargetHealthDescriptions']:
                if instance['TargetHealth']['State'] == 'healthy':
                    instance_ids.append(", ".join(response['Target']['Id']))
            return instance_ids
        except Exception as error:
            raise EnvironmentError(error)

    def deregister_target_group(self, target_group_names: List[str]) -> Dict[str, any]:
        """
        Deregister the specified targets from the specified target group

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.deregister_targets
        :param target_group_names: The AWS name of the target groups
        """
        target_group = self.get_target_groups_arns(target_group_names)
        target_id = self.get_healthy_instances(target_group)

        print(f'Unregistering targets from: {", ".join(target_group_names)}')
        response = self.client.deregister_targets(
            TargetGroupArn=target_group,
            Targets=[{'Id': [target_id]}, ]
        )
        return response

    def register_target_group(self, target_group_names: List[str]) -> Dict[str, any]:
        """
        Registers the specified targets with the specified target group

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.register_targets
        :param target_group_names: The AWS name of the target groups
        """
        target_group = self.get_target_groups_arns(target_group_names)
        target_id = self.get_healthy_instances(target_group)

        print(f'Registering targets to: {", ".join(target_group_names)}')
        response = self.client.register_targets(
            TargetGroupArn=target_group,
            Targets=[{'Id': [target_id]}, ]
        )
        return response

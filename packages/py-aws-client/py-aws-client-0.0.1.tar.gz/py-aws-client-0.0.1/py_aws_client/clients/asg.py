from enum import Enum
from typing import List, Dict, Union

import boto3


class AutoscalingGroup(object):
    class ScalingProcess(Enum):
        """
        Available Scaling Processes that can be Suspended and Resumed.
        https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html
        """
        Terminate = 'Terminate'
        Launch = 'Launch'
        AddToLoadBalancer = 'AddToLoadBalancer'
        AlarmNotification = 'AlarmNotification'
        AZRebalance = 'AZRebalance'
        HealthCheck = 'HealthCheck'
        ReplaceUnhealthy = 'ReplaceUnhealthy'
        ScheduledActions = 'ScheduledActions'

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
                service_name='autoscaling',
            )
        elif region:
            self.client = boto3.client(
                service_name='autoscaling',
                region_name=region
            )

    def describe_auto_scaling_groups(self, autoscaling_group_names: List[str]) -> List[Dict[str, any]]:  # type: ignore
        """
        Describes the given auto-scaling groups

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_groups
        :param autoscaling_group_names: names of asg to describe
        :return: aws describe_auto_scaling_groups response
        """
        print(f'Describing Auto-Scaling Groups for: {", ".join(autoscaling_group_names)}')

        asgs = []
        response = self.client.describe_auto_scaling_groups(
            AutoScalingGroupNames=autoscaling_group_names,
            MaxRecords=100
        )

        next_token = response.get('NextToken')
        asgs += response.get('AutoScalingGroups', [])

        while next_token:
            response = self.client.describe_auto_scaling_groups(
                AutoScalingGroupNames=autoscaling_group_names,
                NextToken=next_token,
                MaxRecords=100,
            )

            next_token = response.get('NextToken')
            asgs += response.get('AutoScalingGroups', [])

        return asgs

    def describe_auto_scaling_instances(self, instance_ids: List[str]) -> Dict[str, any]:  # type: ignore
        """
        Describes the given auto-scaling groups

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_instances
        :param instance_ids: ids of instances to describe
        :return: aws describe_auto_scaling_groups response
        """
        response = self.client.describe_auto_scaling_instances(
            InstanceIds=instance_ids,
        )

        return response

    def describe_tags(self, asg_name: str):
        """
        Describes tags for the given ASG

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_tags

        param asg_name: name of the autoscaling group to describe tags for
        """
        print(f"Describing 100 Tags for ASG. name={asg_name}")
        response = self.client.describe_tags(
            Filters=[
                {
                    'Name': 'auto-scaling-group',
                    'Values': [
                        asg_name,
                    ]
                },
            ],
            MaxRecords=100
        )

        return response

    def suspend_processes(self, autoscaling_group_name: str,
                          scaling_processes: List[ScalingProcess]) -> Dict[str, any]:  # type: ignore
        """
        Suspends Processes on the specified autoscaling group

        https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling
        .Client.suspend_processes :param autoscaling_group_name: name of the autoscaling group to suspend processes
        for :param scaling_processes: Terminate | Launch | AddToLoadBalancer | AlarmNotification | AZRebalance |
        HealthCheck | ReplaceUnhealthy | ScheduledActions :return: suspend processes response
        """
        response = self.client.suspend_processes(
            AutoScalingGroupName=autoscaling_group_name,
            ScalingProcesses=[process.value for process in scaling_processes]
        )

        return response

    def resume_processes(self, autoscaling_group_name: str,
                         scaling_processes: List[ScalingProcess]) -> Dict[str, any]:  # type: ignore
        """
        Resumes Processes on the specified autoscaling group

        https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling
        .Client.resume_processes :param autoscaling_group_name: a list of instance ids to get :param
        scaling_processes: Terminate | Launch | AddToLoadBalancer | AlarmNotification | AZRebalance | HealthCheck |
        ReplaceUnhealthy | ScheduledActions :return: resume processes response
        """
        response = self.client.resume_processes(
            AutoScalingGroupName=autoscaling_group_name,
            ScalingProcesses=[process.value for process in scaling_processes]
        )

        return response

    def set_instance_health(self, instance_id: str, health_status: str,
                            respects_grace_period: bool = True) -> Dict[str, any]:  # type: ignore
        """
        Sets the instance health to the given status.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_instance_health
        :param instance_id: the id of the instance to set health for
        :param health_status: Healthy | Unhealthy
        :param respects_grace_period: should we wait for the asg processes or kick them off?
        :return: set instance health api response
        """
        response = self.client.set_instance_health(
            InstanceId=instance_id,
            HealthStatus=health_status,
            ShouldRespectGracePeriod=respects_grace_period
        )

        return response

    def create_or_update_tags(self, autoscaling_group_name: str,
                              filters: List[Dict[str, Union[str, bool]]]) -> Dict[str, any]:  # type: ignore
        """
        Creates or updates tags for the specified Auto Scaling group
        An existing tag will overwrite the previous tag definition
        If the tag doesn't exist, it is created

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_or_update_tags
        :param autoscaling_group_name: The name of the Auto Scaling group
        :param filters: a list of filters to create/update specific tags
        :return: aws create/update tag response
        """
        print(f'Creating/Updating tags for: {autoscaling_group_name}')
        response = self.client.create_or_update_tags(Tags=filters)

        return response

    def detach_load_balancer_target_groups(self, autoscaling_group_name: str) -> Dict[str, any]:  # type: ignore
        """
        Detaches the specified target group from the specified Auto Scaling group

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancer_target_groups
        :param autoscaling_group_name: The name of the Auto Scaling group
        :return: aws detach_load_balancer_target_groups response
        """
        target_group_arns = self.get_load_balancer_target_group_arns(autoscaling_group_name)

        print(f'Detaching target group {target_group_arns} from the Auto Scaling group: {autoscaling_group_name}')
        response = self.client.detach_load_balancer_target_groups(
            AutoScalingGroupName=autoscaling_group_name,
            TargetGroupARNs=target_group_arns,
        )

        return response

    def attach_load_balancer_target_groups(self, autoscaling_group_name: str) -> Dict[str, any]:  # type: ignore
        """
        Attaches the specified target groups from the specified Auto Scaling group

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancer_target_groups
        :param autoscaling_group_name: The name of the Auto Scaling group
        :return: aws attach_load_balancer_target_groups response
        """
        target_group_arns = self.get_load_balancer_target_group_arns(autoscaling_group_name)

        print(f'Attaching target group {target_group_arns} to the Auto Scaling group: {autoscaling_group_name}')
        response = self.client.attach_load_balancer_target_groups(
            AutoScalingGroupName=autoscaling_group_name,
            TargetGroupARNs=target_group_arns,
        )

        return response

    def describe_load_balancer_target_groups(self, autoscaling_group_name: str) -> Dict[str, any]:  # type: ignore
        """
        Describes the target groups attached to the specified Auto Scaling group

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_load_balancer_target_groups
        :param autoscaling_group_name: The name of the Auto Scaling group
        :return: aws describe_load_balancer_target_groups response
        """
        response = self.client.describe_load_balancer_target_groups(
            AutoScalingGroupName=autoscaling_group_name
        )

        return response

    def get_load_balancer_target_group_arns(self, autoscaling_group_name: str) -> List:
        """
        Gets the ARN of the load balancer target group for the specified Auto Scaling group

        param autoscaling_group_name: The name of the Auto Scaling group
        :return: target_group_arn as a list
        """
        print(f'Getting target group ARN for the Auto Scaling group: {autoscaling_group_name}')
        response = self.client.describe_load_balancer_target_groups(
            AutoScalingGroupName=autoscaling_group_name,
        )

        target_group_arns = []
        for target in response['LoadBalancerTargetGroups']:
            arn = target['LoadBalancerTargetGroupARN']
            target_group_arns.append(arn)

        return target_group_arns

    def update_auto_scaling_group_min_max_desired_counts(self, asg_name: str, minimum: int, maximum: int,
                                                         desired: int) -> Dict[str, any]:  # type: ignore
        response = self.client.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=minimum,
            MaxSize=maximum,
            DesiredCapacity=desired,
        )

        return response

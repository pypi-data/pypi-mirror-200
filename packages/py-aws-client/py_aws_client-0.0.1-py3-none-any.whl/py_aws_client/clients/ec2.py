import boto3
from typing import List, Dict, Optional


class Ec2(object):
    def __init__(self, session: boto3.session.Session = None, region: str = None):
        """
        Initializes an EC2 client using either a boto3 Session or an AWS region.

        This constructor sets up an EC2 client using a boto3 Session object or a specified AWS region.
        If both session and region are provided, it raises an EnvironmentError. The client is created using
        the session if it is provided, otherwise, it is created using the region. If neither session nor
        region is provided, a default client will be created using the default AWS credentials and region.

        :param session: A boto3 Session object used to create the client (optional if region is provided).
        :param region: The AWS region used to create the client (optional if session is provided).
        :raises EnvironmentError: If both session and region are provided
        """
        if session and region:
            raise EnvironmentError('1 of session or region must be provided')

        if session:
            self.client = session.client(
                service_name='ec2',
            )
        elif region:
            self.client = boto3.client(
                service_name='ec2',
                region_name=region
            )

    def get_instances(self, instance_ids: List[str] = None, filters: List[Dict] = None) -> Dict[str, any]:
        """
        Get instance information for ec2 instances

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
        :param instance_ids: a list of instance ids to get
        :param filters: a list of filters to limit instances in the response
        :return: described instances response
        """
        describe_response = self.client.describe_instances(
            InstanceIds=instance_ids if instance_ids else [],
            Filters=filters if filters else [],
        )

        return describe_response

    def wait_for_instances_to_stop(self, instance_ids: List[str]) -> None:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.InstanceStopped
        :param instance_ids: a list of ec2 instance ids to wait for until stopped
        """
        waiter = self.client.get_waiter('instance_stopped')
        waiter.wait(
            InstanceIds=instance_ids,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 60
            }
        )

    def stop_instances(self, instance_ids: List[str], force: bool = False, wait: bool = True) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances
        :param instance_ids: a list of ec2 instance ids to stop
        :param force: should the instances be forcefully stopped?  This is not graceful.
        :param wait: do we want to wait for the instances to stop?
        :return:
        """
        response = self.client.stop_instances(
            InstanceIds=instance_ids,
            Force=force
        )

        if wait:
            self.wait_for_instances_to_stop(
                instance_ids=instance_ids
            )

        return response

    def reboot_instance(self, instance_ids: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.reboot_instances
        :param instance_ids: EC2 instance ID
        """
        response = self.client.reboot_instances(
            InstanceIds=instance_ids
        )

        return response

    def describe_images(self, image_ids: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
        :param image_ids: list of image ids to describe
        :return: described images response
        """
        response = self.client.describe_images(
            ImageIds=image_ids
        )

        return response

    def wait_for_images_to_be_available(self, image_ids: List[str]) -> None:
        """
        Wait for Amazon Machine Images to become available for consumption/use.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.ImageAvailable
        :param image_ids: list of image ids to wait on for availability
        """
        waiter = self.client.get_waiter('image_available')
        waiter.wait(
            ImageIds=image_ids,
            WaiterConfig={
                'Delay': 15,
                'MaxAttempts': 720  # Timeout after 3 hours
            }
        )

    def create_image(self, instance_id: str, name: str, description: str,
                     no_reboot: bool = False, tag_specifications: list = None, wait: bool = True) -> Dict[str, any]:
        """
        Creates an Amazon Machine Image from the given instance id.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_image
        :param instance_id: instance id to create an image from
        :param name: unique name to give the ami
        :param description: how would you describe this ami?
        :param no_reboot: when True, the AMI is not rebooted when the image is created.
        :param tag_specifications: list of tag specs for the resulting snapshot and image.
        :param wait: do we want to wait until the image is available?
        :return: created image response
        """
        if not tag_specifications:
            tag_specifications = []

        response = self.client.create_image(
            InstanceId=instance_id,
            Name=name,
            Description=description,
            NoReboot=no_reboot,
            TagSpecifications=tag_specifications
        )

        if wait:
            image_id = response.get('ImageId')
            self.wait_for_images_to_be_available(
                image_ids=[image_id]
            )

        return response

    def describe_latest_launch_template_version(self, launch_template_id: str) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_launch_template_versions
        :param launch_template_id: id of the launch template to get the latest version of.
        :return:
        """
        response = self.client.describe_launch_template_versions(
            LaunchTemplateId=launch_template_id,
            Versions=[
                '$Latest',
            ]
        )

        return response

    def describe_instance_status(self, instance_ids: List[str]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instance_status
        :param instance_ids:
        :return:
        """
        response = self.client.describe_instance_status(
            InstanceIds=instance_ids
        )

        return response

    def describe_security_groups(self, group_ids: Optional[List[str]] = None, group_names: Optional[List[str]] = None,
                                 filters: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups
        :param group_ids: a list of security group ids to describe
        :param group_names: a list of security group names to describe
        :param filters: a list of filters to limit security groups in the response
        :return: described security groups response
        """
        response = self.client.describe_security_groups(
            GroupIds=group_ids if group_ids else [],
            GroupNames=group_names if group_names else [],
            Filters=filters if filters else [],
        )

        return response

    def describe_vpcs(self, vpc_ids: Optional[List[str]] = None, filters: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        Describes one or more AWS VPCs.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs
        :param vpc_ids: A list of VPC IDs to describe. (optional)
        :param filters: A list of filters to apply to the results. (optional)
        :return: A dictionary containing the VPC information.
        """
        params = {}
        if vpc_ids:
            params['VpcIds'] = vpc_ids
        if filters:
            params['Filters'] = filters

        response = self.client.describe_vpcs(**params)

        return response

    def describe_subnets(self, subnet_ids: Optional[List[str]] = None, filters: Optional[List[Dict]] = None) \
            -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets
        :param subnet_ids: a list of subnet ids to describe
        :param filters: a list of filters to limit subnets in the response
        :return: described subnets response
        """
        response = self.client.describe_subnets(
            SubnetIds=subnet_ids if subnet_ids else [],
            Filters=filters if filters else [],
        )

        return response

    def create_security_group(self, group_name: str, description: str, vpc_id: Optional[str] = None,
                              tag_specifications: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_security_group
        :param group_name: the name of the new security group
        :param description: a description for the new security group
        :param vpc_id: the ID of the VPC, default is your default VPC
        :param tag_specifications: a list of tag specifications for the new security group
        :return: created security group response
        """
        params = {
            "GroupName": group_name,
            "Description": description
        }
        if vpc_id:
            params["VpcId"] = vpc_id
        if tag_specifications:
            params["TagSpecifications"] = tag_specifications

        response = self.client.create_security_group(**params)
        return response

    def delete_security_group(self, group_id: Optional[str] = None, group_name: Optional[str] = None) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_security_group
        :param group_id: the ID of the security group to delete
        :param group_name: the name of the security group to delete
        :return: deleted security group response
        """
        if not group_id and not group_name:
            raise ValueError("Either group_id or group_name must be provided")
        params = {}
        if group_id:
            params["GroupId"] = group_id
        if group_name:
            params["GroupName"] = group_name

        response = self.client.delete_security_group(**params)
        return response

    def authorize_security_group_ingress(self, group_id: Optional[str] = None, group_name: Optional[str] = None,
                                         ip_permissions: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.authorize_security_group_ingress
        :param group_id: the ID of the security group
        :param group_name: the name of the security group
        :param ip_permissions: a list of IP permissions to add to the security group
        :return: authorized security group ingress response
        """
        if not group_id and not group_name:
            raise ValueError("Either group_id or group_name must be provided")

        params = {
            "IpPermissions": ip_permissions if ip_permissions else []
        }
        if group_id:
            params["GroupId"] = group_id
        if group_name:
            params["GroupName"] = group_name

        response = self.client.authorize_security_group_ingress(**params)
        return response

    def revoke_security_group_ingress(self, group_id: Optional[str] = None, group_name: Optional[str] = None,
                                      ip_permissions: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.revoke_security_group_ingress
        :param group_id: the ID of the security group
        :param group_name: the name of the security group
        :param ip_permissions: a list of IP permissions to remove from the security group
        :return: revoked security group ingress response
        """
        if not group_id and not group_name:
            raise ValueError("Either group_id or group_name must be provided")

        params = {
            "IpPermissions": ip_permissions if ip_permissions else []
        }
        if group_id:
            params["GroupId"] = group_id
        if group_name:
            params["GroupName"] = group_name

        response = self.client.revoke_security_group_ingress(**params)
        return response

    def create_tags(self, resources: List[str], tags: List[Dict]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_tags
        :param resources: a list of resource IDs to tag
        :param tags: a list of tags to apply
        :return: created tags response
        """
        response = self.client.create_tags(
            Resources=resources,
            Tags=tags
        )
        return response

    def delete_tags(self, resources: List[str], tags: List[Dict]) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_tags
        :param resources: a list of resource IDs to remove tags from
        :param tags: a list of tags to remove
        :return: deleted tags response
        """
        response = self.client.delete_tags(
            Resources=resources,
            Tags=tags
        )

        return response

    def describe_key_pairs(self, key_names: Optional[List[str]] = None, filters: Optional[List[Dict]] = None)\
            -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_key_pairs
        :param key_names: a list of key pair names to describe
        :param filters: a list of filters to limit key pairs in the response
        :return: described key pairs response
        """
        response = self.client.describe_key_pairs(
            KeyNames=key_names if key_names else [],
            Filters=filters if filters else [],
        )

        return response

    def create_key_pair(self, key_name: str, key_pair_type: Optional[str] = 'rsa') -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_key_pair
        :param key_name: the name of the new key pair
        :param key_pair_type: the type of the key pair, defaults to 'rsa'
        :return: created key pair response
        """
        response = self.client.create_key_pair(
            KeyName=key_name,
            KeyPairType=key_pair_type
        )

        return response

    def delete_key_pair(self, key_name: str) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_key_pair
        :param key_name: the name of the key pair to delete
        :return: deleted key pair response
        """
        response = self.client.delete_key_pair(
            KeyName=key_name
        )

        return response

    def describe_network_interfaces(self, network_interface_ids: Optional[List[str]] = None,
                                    filters: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces
        :param network_interface_ids: a list of network interface IDs to describe
        :param filters: a list of filters to limit network interfaces in the response
        :return: described network interfaces response
        """
        response = self.client.describe_network_interfaces(
            NetworkInterfaceIds=network_interface_ids if network_interface_ids else [],
            Filters=filters if filters else [],
        )

        return response

    def describe_volumes(self, volume_ids: Optional[List[str]] = None, filters: Optional[List[Dict]] = None) \
            -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_volumes
        :param volume_ids: a list of EBS volume IDs to describe
        :param filters: a list of filters to limit volumes in the response
        :return: described volumes response
        """
        response = self.client.describe_volumes(
            VolumeIds=volume_ids if volume_ids else [],
            Filters=filters if filters else [],
        )

        return response

    def create_volume(self, size: int, availability_zone: str, volume_type: Optional[str] = 'gp3',
                      snapshot_id: Optional[str] = None, tags: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_volume
        :param size: the size of the volume, in GiB
        :param availability_zone: the Availability Zone in which to create the volume
        :param volume_type: defaults to 'gp3'
        :param snapshot_id: the ID of the snapshot from which to create the volume, if any
        :param tags: a list of tags to apply to the volume
        :return: created volume response
        """
        params = {
            'Size': size,
            'AvailabilityZone': availability_zone,
            'VolumeType': volume_type
        }

        if snapshot_id:
            params['SnapshotId'] = snapshot_id

        if tags:
            params['TagSpecifications'] = [
                {
                    'ResourceType': 'volume',
                    'Tags': tags
                }
            ]

        response = self.client.create_volume(**params)
        return response

    def delete_volume(self, volume_id: str) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_volume
        :param volume_id: the ID of the EBS volume to delete
        :return: deleted volume response
        """
        response = self.client.delete_volume(
            VolumeId=volume_id
        )

        return response

    def attach_volume(self, instance_id: str, volume_id: str, device: str) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.attach_volume
        :param instance_id: the ID of the instance to which the volume will be attached
        :param volume_id: the ID of the EBS volume to attach
        :param device: the device name to expose to the instance (e.g., '/dev/sdh')
        :return: attached volume response
        """
        response = self.client.attach_volume(
            InstanceId=instance_id,
            VolumeId=volume_id,
            Device=device
        )

        return response

    def detach_volume(self, volume_id: str, instance_id: Optional[str] = None, device: Optional[str] = None,
                      force: bool = False) -> Dict[str, any]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.detach_volume
        :param volume_id: the ID of the EBS volume to detach
        :param instance_id: the ID of the instance from which the volume will be detached
        :param device: the device name to expose to the instance (e.g., '/dev/sdh')
        :param force: force the detachment if the previous detachment attempt did not occur cleanly
        :return: detached volume response
        """
        params = {
            'VolumeId': volume_id,
            'Force': force
        }

        if instance_id:
            params['InstanceId'] = instance_id

        if device:
            params['Device'] = device

        response = self.client.detach_volume(**params)
        return response

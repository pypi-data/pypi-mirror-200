import boto3
from typing import Optional

from .clients import (
    AutoscalingGroup,
    Cloudtrail,
    Cloudwatch,
    Config,
    DynamoDb,
    Ec2,
    Elbv2,
    Glue,
    Iam,
    Ssm,
    Ses,
    Sns,
    Sqs,
    S3,
    SecretsManager
)


class PyAwsClient(object):
    """
    The PyAwsClient is responsible for constructing various AWS API service Clients
    """
    _session: boto3.session.Session

    _region: str
    _profile_name: str

    def __init__(self, region: str, profile_name: Optional[str] = ''):
        """
        Initializes a new PyAwsClient
        The client will create a client with the profile, when the profile is given
        Otherwise it will create a default client using only the region.
        The default client will use the default AWS credentials.
        param region: The aws region to create new client in
        param profile_name: The aws profile to use when interacting against AWS.
        """
        self._region = region
        self._profile_name = profile_name

        if profile_name:
            self._session = boto3.session.Session(
                region_name=region,
                profile_name=profile_name,
            )

    def _get_client(self, client_type: type):
        if self._profile_name:
            return client_type(session=self._session)

        return client_type(region=self._region)

    def asg(self) -> AutoscalingGroup:
        """
        Creates a new AutoScaling client
        """
        return self._get_client(AutoscalingGroup)

    def cloudwatch(self) -> Cloudwatch:
        """
        Creates a new Cloudwatch client
        """
        return self._get_client(Cloudwatch)

    def config(self) -> Config:
        """
        Creates a new Config client
        """
        return self._get_client(Config)

    def cloudtrail(self) -> Cloudtrail:
        """
        Creates a new Cloudtrail client
        """
        return self._get_client(Cloudtrail)

    def dynamodb(self) -> DynamoDb:
        """
        Creates a new DynamoDB client
        """
        return self._get_client(DynamoDb)

    def ec2(self) -> Ec2:
        """
        Creates a new EC2 client
        """
        return self._get_client(Ec2)

    def elbv2(self) -> Elbv2:
        """
        Creates a new Elbv2 (Application Load Balancer) client
        """
        return self._get_client(Elbv2)

    def glue(self) -> Glue:
        """
        Creates a new Glue client
        """
        return self._get_client(Glue)

    def iam(self) -> Iam:
        """
        Creates a new IAM client
        """
        return self._get_client(Iam)

    def ssm(self) -> Ssm:
        """
        Creates a new SSM client
        """
        return self._get_client(Ssm)

    def ses(self) -> Ses:
        """
        Creates a new SES client
        """
        return self._get_client(Ses)

    def s3(self) -> S3:
        """
        Creates a new S3 client
        """
        return self._get_client(S3)

    def secretsmanager(self) -> SecretsManager:
        """
        Creates a new SecretsManager client
        """
        return self._get_client(SecretsManager)

    def sqs(self) -> Sqs:
        """
        Creates a new SQS client
        """
        return self._get_client(Sqs)

    def sns(self) -> Sns:
        """
        Creates a new SNS client
        """
        return self._get_client(Sns)

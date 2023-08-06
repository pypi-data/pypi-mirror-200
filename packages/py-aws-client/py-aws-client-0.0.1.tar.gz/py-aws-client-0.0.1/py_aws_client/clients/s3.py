import boto3
import json
from botocore.exceptions import ClientError
from typing import List, Dict, Optional


class S3(object):
    def __init__(self, session: boto3.session.Session = None, region: str = None):
        """
        Creates a client using either the boto3 Session or region.
        This extended `S3` class includes methods for handling common S3 tasks such as:

        - Listing, creating, and deleting buckets
        - Uploading and downloading files
        - Generating pre-signed URLs for temporary access to objects
        - Copying and deleting objects
        - Managing server-side encryption settings
        - Managing bucket policies and object ACLs
        - Managing CORS configurations for buckets

        These methods provide a more comprehensive interface for working with S3 resources,
        making the class more versatile, optimized, and secure.
        param session: required when no region is provided
        param region: required when no session is provided
        """
        if session and region:
            raise EnvironmentError('1 of session or region must be provided')

        if session:
            self.client = session.client(
                service_name='s3',
            )
        elif region:
            self.client = boto3.client(
                service_name='s3',
                region_name=region
            )

    def list_buckets(self) -> List[str]:
        response = self.client.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]

    def create_bucket(self, bucket_name: str, acl: str = "private") -> Dict[str, str]:
        response = self.client.create_bucket(
            Bucket=bucket_name, ACL=acl, CreateBucketConfiguration={"LocationConstraint": self.client.meta.region_name}
        )
        return response

    def delete_bucket(self, bucket_name: str) -> None:
        self.client.delete_bucket(Bucket=bucket_name)

    def upload_file(self, file_path: str, bucket_name: str, object_key: str, extra_args: Optional[Dict] = None) -> None:
        if extra_args is None:
            extra_args = {}
        self.client.upload_file(file_path, bucket_name, object_key, ExtraArgs=extra_args)

    def download_file(self, bucket_name: str, object_key: str, file_path: str) -> None:
        self.client.download_file(bucket_name, object_key, file_path)

    def generate_presigned_url(self, bucket_name: str, object_key: str, expiration: int = 3600) -> str:
        try:
            response = self.client.generate_presigned_url(
                "get_object", Params={"Bucket": bucket_name, "Key": object_key}, ExpiresIn=expiration
            )
        except ClientError as error:
            raise error

        return response

    def copy_object(self, src_bucket: str, src_key: str, dest_bucket: str, dest_key: str) -> None:
        self.client.copy_object(
            CopySource={"Bucket": src_bucket, "Key": src_key}, Bucket=dest_bucket, Key=dest_key
        )

    def delete_object(self, bucket_name: str, object_key: str) -> None:
        self.client.delete_object(Bucket=bucket_name, Key=object_key)

    def get_bucket_encryption(self, bucket_name: str) -> Dict:
        try:
            response = self.client.get_bucket_encryption(Bucket=bucket_name)
        except ClientError as error:
            if error.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                return {"Status": "Disabled"}
            else:
                raise error
        return response["ServerSideEncryptionConfiguration"]

    def enable_bucket_encryption(self, bucket_name: str, kms_key_id: Optional[str] = None) -> None:
        if kms_key_id:
            sse_algorithm = "aws:kms"
            kms_master_key_id = kms_key_id
        else:
            sse_algorithm = "AES256"
            kms_master_key_id = ""

        self.client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault":
                            {
                                "SSEAlgorithm": sse_algorithm,
                                "KMSMasterKeyID": kms_master_key_id
                            }
                    }
                ]
            },
        )

    def disable_bucket_encryption(self, bucket_name: str) -> None:
        self.client.delete_bucket_encryption(Bucket=bucket_name)

    def get_bucket_policy(self, bucket_name: str) -> Optional[Dict]:
        try:
            response = self.client.get_bucket_policy(Bucket=bucket_name)
            return response
        except ClientError as error:
            if error.response["Error"]["Code"] == "NoSuchBucketPolicy":
                return None
            else:
                raise error

    def put_bucket_policy(self, bucket_name: str, policy: Dict) -> None:
        self.client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))

    def delete_bucket_policy(self, bucket_name: str) -> None:
        self.client.delete_bucket_policy(Bucket=bucket_name)

    def get_object_acl(self, bucket_name: str, object_key: str) -> Dict:
        response = self.client.get_object_acl(Bucket=bucket_name, Key=object_key)
        return response

    def put_object_acl(self, bucket_name: str, object_key: str, acl: str) -> None:
        self.client.put_object_acl(Bucket=bucket_name, Key=object_key, ACL=acl)

    def get_bucket_cors(self, bucket_name: str) -> Dict:
        try:
            response = self.client.get_bucket_cors(Bucket=bucket_name)
            return response
        except ClientError as error:
            if error.response["Error"]["Code"] == "NoSuchCORSConfiguration":
                return {
                    "CORSRules": []
                }
            else:
                raise error

    def put_bucket_cors(self, bucket_name: str, cors_rules: List[Dict]) -> None:
        self.client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration={"CORSRules": cors_rules})

    def delete_bucket_cors(self, bucket_name: str) -> None:
        self.client.delete_bucket_cors(Bucket=bucket_name)

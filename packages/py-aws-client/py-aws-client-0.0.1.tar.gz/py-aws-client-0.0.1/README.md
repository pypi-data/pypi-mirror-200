# py-aws-client
`py-aws-client` is a Python package that provides a high-level wrapper for the Boto3 AWS SDK, allowing for extended customization and ease of use. It simplifies the process of creating and interacting with various AWS API service clients by providing a simple and consistent interface. The package includes pre-configured clients for commonly used AWS services such as Auto Scaling, CloudWatch, DynamoDB, EC2, S3, and more. It also handles common AWS authentication mechanisms and can be used with either a default profile or a specified profile.

## Installation
You can install `py-aws-client` using pip:

```
pip install py-aws-client
```

## Usage
Here's an example of how to use `py-aws-client` to interact with AWS services:

```python

from py_aws_client import PyAwsClient

# Create a new client with the default profile
client = PyAwsClient(region='us-east-1')

# Create a new EC2 client
ec2 = client.ec2()

# List all instances
instances = ec2.describe_instances()

for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
```
In this example, we create a new `PyAwsClient` instance with the default profile and use it to create a new `EC2` client. 
We then use the `describe_instances` method to retrieve information about all EC2 instances in the region and print out their instance IDs and states.

You can also use a named profile by passing the `profile_name` parameter to the `PyAwsClient` constructor:

```python
# Create a new client with a named profile
client = PyAwsClient(region='us-east-1', profile_name='my-profile')
```

## License
This package is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
If you have suggestions for new features, bug fixes, or other improvements, please open an issue or pull request on GitHub.

## Acknowledgements
`py-aws-client` is built using the Boto3 AWS SDK and would not be possible without the hard work of the Boto3 team and the AWS community. Thank you for your contributions!
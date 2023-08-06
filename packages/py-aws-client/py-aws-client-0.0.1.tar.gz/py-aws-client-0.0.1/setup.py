import os
from setuptools import setup, find_packages
from distutils.command.upload import upload
from distutils.command.register import register


class Register(register):

    @staticmethod
    def _get_rc_file():
        return os.path.join('.', '.pypirc')


class Upload(upload):

    @staticmethod
    def _get_rc_file():
        return os.path.join('.', '.pypirc')


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='py-aws-client',
    version='0.0.1',
    description='py-aws-client is a Python package that simplifies the process of creating and interacting with various AWS API service clients by providing a high-level wrapper for the Boto3 AWS SDK. It includes pre-configured clients for commonly used AWS services and handles common AWS authentication mechanisms. Suitable for both novice and experienced developers looking to integrate AWS services into their Python applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ladycami/py-aws-client',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    cmdclass={
        'register': Register,
        'upload': Upload,
    }
)

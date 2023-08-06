## Project description
[![version](https://img.shields.io/badge/python-3.10-green)](https://semver.org)
[![version](https://img.shields.io/badge/boto%5Bs3%5D-1.26.87-green)](https://semver.org)
[![version](https://img.shields.io/badge/unittest-latest-green)](https://semver.org)

## Custom package for AWS Services 
[My custom awsservice on PYPI](https://pypi.org/project/awsservice/)

[SETUPTOOLS docs](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html)
## Getting Started
Assuming that you have a supported version of Python installed, you can first set up your environment with:

```shell
$ python -m venv .venv
...
$ . .venv/bin/activate
```

Then, you can install aws-service from PyPI with:
```shell
$ python -m pip install awsservice
```

or install from S3 source with:
[url](https://blog.knoldus.com/packaging-hosting-python-repo-to-s3/)


## Using AWS-service
After installing the package: 

Set up credentials (in e.g. ~/.aws/credentials):

- aws_access_key_id = YOUR_KEY
- aws_secret_access_key = YOUR_SECRET
- Then, set up a default region (in e.g. ~/.aws/config):
- region=us-east-1

Other credentials configuration method can be found here

Then, from a Python interpreter you can import it and use its classes and functions::
```shell
>>> from awsservice.ec2_service import Ec2Service
>>> from awsservice.s3_service import S3Service
>>> from awsservice.cloudwatch_service import CloudwatchService
>>> my_s3 = S3Service()
>>> my_s3.create_new_bucket(bucket_name='my_new_bucket', region='eu-west-2')
>>> my_s3.put_file( file_name='file_1', bucket='my_new_bucket', object_name='custom-name')
```

## Availible modules:

### Class S3Service (module s3_service)
Functionality (availible methods): 
* [create_new_bucket]() - create new bucket 
* [put_file]() - upload file on s3 
* [get_file]() - download file from s3
* [check_exist]() - check if file exists on s3


### Class Ec2Service (module ec2_service)
Functionality (availible methods): 
* [start_instance]() - start ec2 instance
* [stop_instance]() - stop instance
* [reboot_instance]() - reboot instance
* [get_one_instance_status]() - get one instance status
* [all_instances]() - list all my ID's instances
* [create_my_instance]() - create_instance


### Class CloudwatchService (module cloudwatch_service)
Functionality (availible methods): 

* [get_cpu_usage_2]() - get cpu usage, version 2
* [get_cpu_usage]() - get cpu usage, version 1

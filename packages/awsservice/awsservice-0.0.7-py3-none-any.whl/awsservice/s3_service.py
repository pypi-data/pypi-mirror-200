import os

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def create_new_bucket(self, bucket_name: str, region: str = 'eu-west-2') -> bool:
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (eu-west-2).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """
        try:
            location = {'LocationConstraint': region}
            self.s3_client.create_bucket(Bucket=bucket_name,
                                         CreateBucketConfiguration=location)
            return True
        except ClientError as e:
            return e

    def put_file(self, file_name: str, bucket: str, object_name=None) -> bool:
        """Upload a file to an S3 bucket

        :param file_name: File to upload.  Located in folder  /media
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # check if file exist
        file_path = os.path.join('./media/', file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        try:
            self.s3_client.upload_file(file_path, bucket, object_name)
            return True
        except EndpointConnectionError as e:
            return e
        except ClientError as e:
            return e

    def get_file(self, bucket_name: str, object_name: str) -> bool:
        """ Download file from S3 bucket to folder /media

        :param bucket_name: Name of Bucket
        :param object_name: File to download
        :return: True if file was Dowloaded, else False
        """
        try:
            # create folder (bucket-name), for download files
            if not os.path.exists(f'./media/{bucket_name}'):
                os.mkdir(f'./media/{bucket_name}')

            # check if file exists in bucket, before get(download) from s3
            if not self.check_exist(object_name, bucket_name):
                raise FileNotFoundError

            # download file to folder /media/bucket_name/
            file_path = os.path.join('./media/', bucket_name, object_name)
            with open(file_path, 'wb') as f:
                self.s3_client.download_fileobj(bucket_name, object_name, f)

            # check if file exist (if was saved to /media)
            if not os.path.exists(file_path):
                raise FileNotFoundError
            return True
        except ClientError as e:
            return e

    def check_exist(self, file_name: str, bucket: str) -> bool:
        try:
            # get list of all objects from bucket
            objs = self.s3_client.list_objects(Bucket=bucket)
            list_keys_in_bucket = [obj['Key'] for obj in objs['Contents']]

            # check if object exist
            if file_name in list_keys_in_bucket:
                return True
            else:
                return False
        except ClientError as e:
            return False

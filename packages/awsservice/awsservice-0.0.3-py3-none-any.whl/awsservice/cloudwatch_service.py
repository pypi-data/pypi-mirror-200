from datetime import datetime, timedelta, timezone
import logging.config
import boto3
import pytz
from botocore.exceptions import ClientError, EndpointConnectionError


class CloudwatchService:
    def __init__(self, region='us-east-1'):
        self.region = region
        self._cloud_watch_client = None

    @property
    def cloud_watch_client(self):
        if not self._cloud_watch_client:
            self._cloud_watch_client = boto3.client("cloudwatch", region_name=self.region)
        return self._cloud_watch_client

    def get_cpu_usage(self, instance_id: str):
        """  Function to get CPU usage of EC2 instance

        This function is implemented by 'get_metric_data':
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_data.html
        :param instance_id: instance_id
        :return:
        """
        try:
            end_time = datetime.now(tz=pytz.UTC)
            start_time = end_time - timedelta(minutes=10)

            response = self.cloud_watch_client.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'cpu_v1',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EC2',
                                'MetricName': 'CPUUtilization',
                                'Dimensions': [
                                    {
                                        'Name': 'InstanceId',
                                        'Value': instance_id
                                    },
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Average',
                            'Unit': 'Percent'
                        },
                        'ReturnData': True,
                    },
                ],
                StartTime=start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                EndTime=end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                # NextToken='string',
                ScanBy='TimestampDescending',
                MaxDatapoints=13,
                # LabelOptions={'Timezone': 'timezone'}
            )
            cpu_load_average = response['MetricDataResults'][0]['Values'][0]
            # return response['MetricDataResults']#[0]['Values']
            return '{:.2f}'.format(cpu_load_average)
        except (ClientError, EndpointConnectionError) as e:
            return e

    def get_cpu_usage_2(self,
                        instance_id: str,
                        minutes_timedelta: int = 10):
        """
        Function to get CPU usage
        time stamp must be in ISO 8601 UTC format (for example, 2016-10-03T23:00:00Z).
        This function is implemented by 'get_metric_statistics':
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_statistics.html
        :param minutes_timedelta: timedelta in minutes, define start time
        :param instance_id: instance_id
        :return: Percents of CPU usage /OR Results List of Timestamps
         example: [{'Timestamp': datetime, 'Average': 0.16, 'Maximum': 0.166, 'Unit': 'Percent'}]
        """
        try:
            end_time = datetime.now(tz=pytz.UTC)
            start_time = end_time - timedelta(minutes=minutes_timedelta)

            response = self.cloud_watch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    },
                ],
                StartTime=start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                EndTime=end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                Period=60,
                Statistics=['Maximum', 'Average'],
                Unit='Percent'
            )
            cpu_load_average = response['Datapoints'][0]['Average']
            # return response['Datapoints'] # return all data from response
            return '{:.2f}'.format(cpu_load_average)
        except ClientError as e:
            return e

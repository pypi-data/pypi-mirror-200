import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


class Ec2Service:
    def __init__(self, region="eu-west-1"):
        self.region = region
        self._ec2_client = None
        self._account_id = None

    @property
    def ec2(self):
        if not self._ec2_client:
            self._ec2_client = boto3.client("ec2", region_name=self.region)
        return self._ec2_client

    @property
    def account_id(self) -> str:
        """
        Returns details about the IAM user or role whose credentials are used to call the operation.
        $ aws sts get-caller-identity      # command in console to get
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_caller_identity.html
        :return: ID of account (12-digits)
        """
        if not self._account_id:
            self._account_id = boto3.client('sts').get_caller_identity().get('Account')
        return self._account_id

    def get_one_instance_status(self, instance_id: str) -> str:
        response = self.ec2.describe_instance_status(InstanceIds=[instance_id])
        return response['InstanceStatuses'][0]['InstanceState']['Name']

    def describe_one_instance(self, instance_id: str):
        """
        Get info about instance
        :return:
        """
        try:
            return self.ec2.describe_instances(
                InstanceIds=[instance_id, ]
            )
        except ClientError as e:
            return e

    def all_instances(self) -> list:
        """
        Function to return List[ID's] of all instances.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeInstances.html
        :return: list of all instances
        """
        response = self.ec2.describe_instances(
            DryRun=False,
            MaxResults=12
        )
        return [item['Instances'][0]['InstanceId'] for item in response['Reservations']]

    def start_instance(self, id_instance: str, dry_run: bool = False) -> str:
        """
        Function to Start one instance
        :param id_instance: id_instance
        :param dry_run: Checks whether you have the required permissions for the action
        :return: status
        """
        response = self.ec2.start_instances(
            InstanceIds=[id_instance],
            # AdditionalInfo='string',
            DryRun=dry_run)
        status = response['StartingInstances'][0]['CurrentState']['Name']
        return status

    def stop_instance(self,
                      instance_id: str,
                      hibernates: bool = True,
                      dry_run: bool = False,
                      force: bool = True) -> dict:
        """
        function to stop One instance
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/stop_instances.html

        :param instance_id:  instance id
        :param instanceId: str - instanceId
        :param hibernates: Сплячий режим Hibernates the instance if the instance was enabled for hibernation at launch.
        :param dry_run:
        :param force:
        :return: status
        """
        try:
            response = self.ec2.stop_instances(
            InstanceIds=[instance_id],
            Hibernate=False,
            DryRun=dry_run,
            Force=force
        )
            # status = response['StoppingInstances'][0]['Name']
            return response
        except Exception as err:
            return err

    def reboot_instance(self, instance_id: str) -> bool:
        try:
            response = self.ec2.reboot_instances(
                InstanceIds=[instance_id, ],
                DryRun=False
            )
            return True
        except ClientError as e:
            return e

    def create_my_instance(self,
                           ami_id: str = 'ami-0c55b159cbfafe1f0',
                           availib_zone: str = 'eu-west-1a',
                           inst_type: str = 't2.micro') -> dict:
        """
        Function to create one Instance - boto3.client
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_instances.html

        For using   boto3.resource:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_instances.html

        :param ami_id:  ID of the AMI.
        :param inst_type: type of hard drive, that we want to create
        :param availib_zone: it's not REGION !
        :return:
        """
        try:
            responce = self.ec2.run_instances(
                ImageId=ami_id,  # ID of the AMI.
                InstanceType=inst_type,
                MaxCount=1,
                # ClientToken='string',
                MinCount=1,
                Placement={
                    'AvailabilityZone': availib_zone,
                    'Affinity': 'string',
                    'GroupName': 'string',
                    'PartitionNumber': 123,
                    'HostId': 'string',
                    'Tenancy': 'default',
                    # 'SpreadDomain': 'string', # Reserved for future use
                    'HostResourceGroupArn': 'string',
                    'GroupId': 'string'
                })
            return responce
        except Exception as e:
            raise e

import os
import sys
import logging
import logging.config
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Add path of parent directory and load env variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()
print(os.getenv('LOGGER_CONFIG_PATH'))

# Configure logging
logging.config.fileConfig(os.getenv('LOGGER_CONFIG_PATH'))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class S3Boto:
    '''
    S3 Bucket Interface for communication with localstack mock of AWS. S3Boto uses the
    singleton principle and only creates one instance. Due to credentials not being 
    changed the singleton principle is a good fit to this usecase.
    '''
    _instance = None
    def __new__(cls, conn_url, access_key_id, access_secret_key):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = boto3.client(
                service_name='s3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=access_secret_key,
                endpoint_url=conn_url
            )
        return cls._instance
    
    def list_buckets(self):
        '''
        List all buckets existing in the connected host
        '''
        try:
            logger.info("Request list of buckets")
            response = self._client.list_buckets()
            return [bucket['Name'] for bucket in response['Buckets']]
        except ClientError as e:
            logger.error(e)
    
    def create_bucket(self, access_level: str, bucket_name: str) -> None:
        '''
        Create new bucket with specified access_level, given the bucket_name
        '''
        try:
            logger.info("Creating bucket")
            self._client.create_bucket(ACL=access_level, Bucket=bucket_name)
        except ClientError as e:
            logger.error(e)
        
    def delete_bucket(self, bucket_name: str) -> None:
        '''
        Delete a bucket given the bucket name
        '''
        try:
            logger.info("Deleting bucket")
            self._client.delete_bucket(Bucket=bucket_name)
        except ClientError as e:
            logger.error(e)

    def upload_file(self, file_name: str, bucket: str, object_name: str = None) -> bool:
        '''
        Upload file to bucket given bucket name. If object_name is provided, set the name
        of the file in the bucket to be object_name, otherwise keep original file name.
        '''
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            logger.info(f"Uploading file: {file_name} to bucket: {bucket}")
            self._client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logger.error(e)
            return False
        
        return True
    
    def read_file(self, bucket_name: str, object_name: str) -> str:
        '''
        Read the content of the file as a UTF-8 encoded string
        '''
        try:
            logger.info(f"Reading file: {object_name} to bucket: {bucket_name}")
            response = self._client.get_object(Bucket=bucket_name, Key=object_name)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            logger.error(e)

import os
from dotenv import load_dotenv
import boto3

# load env variables
load_dotenv()

# get aws credentials vars
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_REGION = os.getenv("AWS_REGION_NAME")
# get aws client session

class AWSClient:
    def getAWSS3Client() -> boto3.session.Session.client:
        try:
            aws_client = boto3.client("s3")

            return aws_client
        except Exception as e:
            print(f"An error as occur while instance a aws client: {e}")
import boto3

class S3Repository:
    def __init__(self, s3_client: boto3.session.Session.client):
        # instance aws session
        self._client = s3_client

    @property
    def client(self):
        return self._client
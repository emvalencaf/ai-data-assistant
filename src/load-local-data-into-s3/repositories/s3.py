from aws.aws_client import getAWSS3Client

class S3Repository:
    def __init__(self):
        # instance aws session
        self._client = getAWSS3Client()

    @property
    def client(self):
        return self._client
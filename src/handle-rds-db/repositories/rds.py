import boto3

class RDSRepository:
    def __init__(self, rds_client: boto3.session.Session.client):
        # instance aws session
        self._client = rds_client

    @property
    def client(self):
        return self._client
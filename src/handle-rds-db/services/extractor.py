import pandas as pd
import os
from io import BytesIO
from repositories.s3 import S3Repository

class ExtractorService:
    def __init__(self, s3Repository: S3Repository) -> None:
        self._repositories = {
            "s3": s3Repository.client
        }
    
    def _getObjectFromBucket(self) -> bytes:
        bucketName = os.getenv("BUCKET_NAME")
        objectKey = os.getenv("OBJECT_KEY")

        # get object from bucket
        res = self._repositories['s3'].get_object(Bucket=bucketName,
                                                  Key=objectKey)
        
        return res['Body'].read()
    
    def getObjectToDataframe(self) -> pd.DataFrame:
        obj_data = self._getObjectFromBucket()

        # convert obj to dataframe
        df = pd.read_csv(BytesIO(obj_data))

        return df
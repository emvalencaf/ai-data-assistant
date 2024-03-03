from botocore.exceptions import ClientError
from datetime import datetime
import os

# repository
from repositories.s3 import S3Repository

class LoaderService:
    def __init__(self, s3Repository: S3Repository):
        
        self._repositories = {
            "s3": s3Repository.client
        }
    
    # load files by a list of files
    def loadFiles(self,
                  filesPath:list[str],
                  bucketName:str,s3_zone:str):
        if not filesPath or len(filesPath) == 0:
            raise ValueError("You must have a least one file to be uploaded in s3")
        
        if not bucketName:
            raise ValueError("You must inform the bucket name in your S3")
        
        if not s3_zone:
            raise ValueError("You must inform the S3 zone where you will uploaded the file")

        if not self._isBucketExists(bucketName=bucketName):
            print(f"[System]: there isn't a bucket named {bucketName}...")
            self._createBucket(bucketName=bucketName)

        # load all files
        for filePath in filesPath:
            self._uploadObject(filePath=filePath,
                               bucketName=bucketName,
                               s3_zone=s3_zone)

    # loading an object into s3
    def _uploadObject(self,
                      filePath:str,
                      bucketName:str, s3_zone:str):
        if not filePath:
            raise ValueError("You must have a file to be uploaded in s3")
        
        if not bucketName:
            raise ValueError("You must inform the bucket name in your S3")
        
        if not s3_zone:
            raise ValueError("You must inform the S3 zone where you will uploaded the file")
    
        filename = os.path.basename(filePath)
        filetype = filename.split(".")[1]

        # current date
        current_date = datetime.now()

        keyS3 = f"{s3_zone}/{filetype.upper()}/{filename.split('.')[0].capitalize()}/{current_date.year}/{current_date.month}/{current_date.day}/{filename}"

        try:
            print(f'[System]: start to load the {filename} (located at: {filePath})...')
            self._repositories['s3'].upload_file(Filename=filePath,
                                                 Bucket=bucketName,
                                                 Key=keyS3)
            print(f'[System]: The {filename} was successfully uploaded to {bucketName}/{keyS3}')
        except Exception as e:
            print(e)
        
    # create a bucket in s3
    def _createBucket(self, bucketName:str):
        if not bucketName:
            raise ValueError("You must inform the bucket name in your S3")
        
        self._repositories['s3'].create_bucket(Bucket=bucketName)

        print(f'[System]: the bucket named {bucketName} was successfully created.')

    # check if a bucket exists in the s3
    def _isBucketExists(self, bucketName:str) -> bool:
        try:
            print(f"[System]: checking if there is a bucket named {bucketName} in the S3...")

            self._repositories['s3'].head_bucket(Bucket=bucketName)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(e)
                return False
            else:
                raise Exception(e)
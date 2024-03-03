import argparse, sys
import os

# app
from modules.ingestLocalData import ingestLocalDataApp

def main():
    # Command Line Interface (CLI) setup
    parser = argparse.ArgumentParser(description="Script to upload CSV files in batch to Amazon S3 buckets")

    parser.add_argument("-b", "--bucketName", required=False, help="Amazon S3 bucket")
    parser.add_argument("-idir","--inputDir", required=False, help="The relative path to the directory of the files you want to upload")
    parser.add_argument("-z","--zone", required=False, help="Name the zone which the objects will be uploaded")    

    args = parser.parse_args()

    if not args.bucketName and not os.getenv("AWS_S3_BUCKET_NAME"):
        print("You must pass a Amazon S3 bucket name as arg or as an env variable")
        sys.exit()

    if not args.inputDir and not os.getenv("INPUT_DIRFILES"):
        print("You must inform in which directory the files you wanted to upload into S3 are")
        sys.exit()

    if not args.zone and not os.getenv("S3_ZONE"):
        print("You must inform in which zone your files will be uploaded at the S3 bucket")

    bucketName = args.bucketName or os.getenv("AWS_S3_BUCKET_NAME")
    dirfiles = args.inputDir or os.getenv("INPUT_DIRFILES")
    s3_zone = args.zone or os.getenv("S3_ZONE")

    ingestLocalDataApp.uploadFilesFromLocalDir(dirFiles=dirfiles,
                                               bucketName=bucketName,
                                               s3_zone=s3_zone)

if __name__ == "__main__":
    main()
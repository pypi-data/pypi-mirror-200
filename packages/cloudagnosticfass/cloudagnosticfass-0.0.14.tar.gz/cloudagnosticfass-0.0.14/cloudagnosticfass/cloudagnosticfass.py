from google.cloud import storage
import boto3
import botocore
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def quicktext():
    print('Hello, Welcome To Serverless Cloud Agnostic Python Package.')



def move_file(cloud,bucket_name, blob_name, destination_bucket_name, destination_blob_name,):
    if cloud == "GCP":
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(bucket_name)
        source_blob = source_bucket.blob(blob_name)
        destination_bucket = storage_client.bucket(destination_bucket_name)
        destination_generation_match_precondition = 0

        blob_copy = source_bucket.copy_blob(source_blob, destination_bucket, destination_blob_name, if_generation_match=destination_generation_match_precondition,)
        source_bucket.delete_blob(blob_name)

        print(
        "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )

    elif cloud == "AWS":
        s3 = boto3.resource('s3')
        source = {'Bucket': bucket_name, 'Key': blob_name}
        try:
            s3.meta.client.copy(source, destination_bucket_name, blob_name)
            logger.info("File copied to the destination bucket successfully!")
        
        except botocore.exceptions.ClientError as error:
            logger.error("There was an error copying the file to the destination bucket")
            print('Error Message: {}'.format(error))
        
        except botocore.exceptions.ParamValidationError as error:
            logger.error("Missing required parameters while calling the API.")
            print('Error Message: {}'.format(error))

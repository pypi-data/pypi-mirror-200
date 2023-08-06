#from google.cloud import storage
import boto3
import botocore
import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')

def quicktext():
    print('Hello, Welcome To Serverless Cloud Agnostic Python Package.')



def move_file(cloud,bucket_name, blob_name, destination_bucket_name, destination_blob_name):
    if cloud == "GCP":
        print("Google code started now")
    
    elif cloud == "AWS":
        print("AWS code started now")
        logger.info("New files uploaded to the source bucket.")
        
        dest_bucket = destination_bucket_name
        source_bucket = bucket_name
        key = blob_name        
        source = {'Bucket': source_bucket, 'Key': key}
        
        try:
            response = s3.meta.client.copy(source, dest_bucket, key)
            logger.info("File copied to the destination bucket successfully!")
            print("File copied to the destination bucket successfully!!")

        except botocore.exceptions.ClientError as error:
            logger.error("There was an error copying the file to the destination bucket")
            print('Error Message: {}'.format(error))

        except botocore.exceptions.ParamValidationError as error:
            logger.error("Missing required parameters while calling the API.")
            print('Error Message: {}'.format(error))
            print('Printing message inside ',cloud,' move file function')
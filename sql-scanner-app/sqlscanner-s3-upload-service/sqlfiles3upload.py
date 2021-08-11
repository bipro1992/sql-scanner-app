import json
import base64
import boto3
import os

BUCKET_NAME = os.environ['SQL_STORE_BUCKET']

def uploadFile(event,context):
    print(event)
    if (event['headers']['content-type']).strip().lower()=='application/x-sql':
        file_content = base64.b64decode(event['body'])
        file_path = event['pathParameters']['name']+'.sql'
        s3 = boto3.client('s3')
        try:
            s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=file_content)
        except Exception as e:
            raise IOError(e)
    else:
        return "Invalid file type"

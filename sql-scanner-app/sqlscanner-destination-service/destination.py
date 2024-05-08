import json
import base64
import boto3
import os
#importing date time
import datetime

BUCKET_NAME = os.environ['SQL_STORE_BUCKET']

snsClient = boto3.client('sns')

def dest(event,context):
    fileName=event['Records'][0]['s3']['object']['key'].replace('_SCAN_REPORT.txt','.sql')
    print(fileName)
    s3=boto3.resource('s3')
    bucket=s3.Bucket(BUCKET_NAME)
    bucket.delete_objects(
    Delete={
        'Objects': [
            {
                'Key': fileName
            },
        ],
        'Quiet': True
    })

    response = snsClient.publish(
    TopicArn=os.environ['TOPIC_ARN'],
    Message='Scan report for '+fileName+' is placed at S3 bucket '+os.environ['SQL_SCAN_STORE_BUCKET']+'. Reach out to AWS admin in order to recieve copy of report.',
    Subject='SQL Scan Notification'
    )

    return response

# importing the boto3 library
import boto3
import re
import os
import logging
logger = logging.getLogger()
# connect to S3 using boto3 client
def sqlChangesScanAndReport(event, context):
  s3=boto3.resource('s3')
  bucket=s3.Bucket(os.environ['SQL_STORE_BUCKET'])
  object_summary_iterator = bucket.objects.all()
  for sqlFile in object_summary_iterator:
    if(sqlFile.key.strip().endswith('.sql')):
    #Read a text file line by line using splitlines object
      fileNameWithPath='/tmp/'+sqlFile.key.replace('.sql','')+'_SCAN_REPORT.txt'
      fileName=sqlFile.key.replace('.sql','')+'_SCAN_REPORT.txt'
      fWrite=open(fileNameWithPath,'w')
      track=[]
      for line in sqlFile.get()["Body"].read().splitlines():
        try:
          each_line = line.decode('utf-8')
          createSearchCriteria=re.search(os.environ['CREATE_REGEX'],each_line.lower())
          if createSearchCriteria:
            data=createSearchCriteria.group(7).split('.')
            if len(data)>0:
                track.append(re.search(os.environ['OBJ_REGEX'],data[-1]).group(2))
            else:
                raise Exception('PATTERN MISMATCH')
          else:
            alterSearchCriteria=re.search(os.environ['ALTER_REGEX'], each_line.lower())
            if alterSearchCriteria and (re.search(os.environ['OBJ_REGEX'],alterSearchCriteria.group(7)).group(2) not in track):
              fWrite.write(each_line)
              logger.info(each_line)
        except:
          logger.error('Error occured')
      fWrite.close()
      s3.Bucket(os.environ['SQL_SCAN_STORE_BUCKET']).upload_file(fileNameWithPath, fileName)
    else:
      logger.info('Not an SQL file')

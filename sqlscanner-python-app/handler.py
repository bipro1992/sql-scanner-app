# importing the boto3 library
import boto3
import re
import os
# connect to S3 using boto3 client
def sqlChangesScanAndReport(event, context):
  s3=boto3.resource('s3')
  bucket=s3.Bucket('sqlscanlist')
  object_summary_iterator = bucket.objects.all()
  for sqlFile in object_summary_iterator:
    if(sqlFile.key.strip().endswith('.sql')):
    #Read a text file line by line using splitlines object
      fileNameWithPath='/tmp/'+sqlFile.key.replace('.sql','')+'_SCAN_REPORT.txt'
      fileName=sqlFile.key.replace('.sql','')+'_SCAN_REPORT.txt'
      fWrite=open(fileNameWithPath,'w')
      track=[]
      for line in sqlFile.get()["Body"].read().splitlines():
        each_line = line.decode('utf-8')
        createSearchCriteria=re.search(os.environ['CREATE_TABLE_REGEX'],each_line.lower())
        if createSearchCriteria:
          data=createSearchCriteria.group(7).split('.')
          if len(data)>0:
              track.append(re.search(os.environ['TABLE_REGEX'],data[-1]).group(2))
          else:
              raise Exception('TABLE PATTERN MISMATCH')
        else:
          alterSearchCriteria=re.search(os.environ['ALTER_TABLE_REGEX'], each_line.lower())
          if alterSearchCriteria and (re.search(os.environ['TABLE_REGEX'],alterSearchCriteria.group(7)).group(2) not in track):
            fWrite.write(each_line)
      fWrite.close()
      s3.Bucket('sqlscanreport').upload_file(fileNameWithPath, fileName)

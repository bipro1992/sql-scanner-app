# SQL-Scanner-App

SQL Scanner App is a tool which scans single consolidated SQL file containing non-production SQL changes yet to deploy in production, and provides SQL scan report to respective person of interest, for e.g. DW team.

SQL scan report contains details on changes made to existing table/procedure/function in production environment. From the scan report one can easily verify if they need to make any required changes in their existing queries and implement changes to exact places.

Application is based on [Python](https://www.python.org/downloads/release/python-380/), [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) and [Serverless Framework](https://www.serverless.com/framework/docs/) , with [AWS](https://aws.amazon.com/) as provider.

# Workflow

![Image of workflow](https://github.com/bipro1992/sqlscanner-python-app/blob/main/workflow.jpg)

# AWS-CDK-PredefindS3
Python Construct class with commonly used configurations for s3 buckets. 
# Using the Module 

1. Add the following in your cdk's  requirements.txt
```
PredefinedS3 @ git+https://github.com/snemir2/AWS-CDK-PredefindS3
```
2. Install requirements
```
pip install -r requirements.txt
```

3. In your CDK stack, import and use the needed modules
`from PredefinedS3 import common_buckets_config`

4. To create a bucket of a given "type", in your cdk stack  instantiate the S3 bucket
```
 s3_access_log_bucket=common_buckets_config(self,"S3AccessLogBucket", "s3-access-logs", "s3_access_log_bucket")
 ```
This should provision a bucket called `s3-access-logs-<account>-<region>` with setting typical for bucket for s3 access logs. 


#Descriptions of each bucket type config

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

## S3 Bucket Types and Settings

| **Setting** | **Data Bucket** | **S3 Access Log Bucket** | **Log Bucket** |
|-------------|------------------|---------------------------|----------------|
| **Public Access** | Blocked | Blocked | Blocked |
| **Encryption** | DSSE_MANAGED | DSSE_MANAGED | DSSE_MANAGED |
| **SSL Enforcement** | ✅ Enabled | ✅ Enabled | ✅ Enabled |
| **Versioning** | ✅ Enabled | ❌ Disabled | ❌ Disabled |
| **Access Control** | Default | LOG_DELIVERY_WRITE | Default |
| **Server Access Logs** | ✅ Enabled | ❌ Not configured | ❌ Not configured |
| **Access Logs Location** | `s3://{log_bucket_name}/{bucket_name}-{account_id}-{region}/` | N/A | N/A |
| **Intelligent Tiering** | ✅ Enabled (0 days) | ❌ Not configured | ❌ Not configured |
| **Lifecycle Rules** | | | |
| - **Transition to Glacier** | 1 year (noncurrent versions) | 1 year | 1 year |
| - **Expiration** | 3 years | 3 years | 3 years |
| - **Noncurrent Version Expiration** | 3 years | ❌ Not configured | ❌ Not configured |
| **Backup Tags** | BackupPlan: Default | ❌ Not configured | ❌ Not configured |
| **Use Case** | General data storage | S3 access logs storage | Application logs storage |

### Access Logs Details:

**Data Bucket Access Logs Path:**
- **Log Bucket**: `s3-access-logs-{account_id}-{region}` (if LZA=False) or `aws-accelerator-s3-access-logs-{account_id}-{region}` (if LZA=True)
- **Log Prefix**: `{bucket_name}-{account_id}-{region}/`
- **Full Path**: `s3://{log_bucket_name}/{bucket_name}-{account_id}-{region}/`

**Example:**
- If bucket name is "my-data-bucket" in account "123456789012" and region "us-east-1"
- Access logs will be stored at: `s3://s3-access-logs-123456789012-us-east-1/my-data-bucket-123456789012-us-east-1/`

The other bucket types (S3 Access Log Bucket and Log Bucket) do not have server access logs configured as they are typically used to store logs themselves.

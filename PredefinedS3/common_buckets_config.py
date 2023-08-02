#Functions to create s3 buckets with configs optimized
#for specific  use cases
#Always appending <region>-<account_id> to the bucket name
#import aws_cdk 

from constructs import Construct
import aws_cdk, time
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
    aws_kms as kms,
    Aws,
    RemovalPolicy,
    aws_ssm as ssm
)

#__version__=time.strftime("%Y.%m")
__version__="2023.07"
class  predefined_bucket(Construct):
    #unset IF not using LZA https://aws.amazon.com/solutions/implementations/landing-zone-accelerator-on-aws/
    LZA=True
    
    def __init__(self, scope: Construct, construct_id: str,
                 bucket_name: str, bucket_type: str ,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        ACCOUNT_ID=Aws.ACCOUNT_ID
        REGION=Aws.REGION 
        #appending <region>-<account_id> to the bucket name
        bucket_unique_name=bucket_name +  "-" + ACCOUNT_ID + "-" + REGION
        ### NOTE: if not using LZA, need to create a bucket for access logs separately. 
        if self.LZA:
            self.log_bucket_name = "aws-accelerator-s3-access-logs-"  + ACCOUNT_ID + "-" + REGION
        else:
            self.log_bucket_name = "s3-access-logs-"  + ACCOUNT_ID + "-" + REGION

        # call the right function based on the bucket type
        #using name withouth region/account_id as code downstream breaks if runtime variables are used. 
    
           
        if bucket_type == "s3_access_log_bucket":
            my_bucket=self.s3_access_log_bucket(bucket_name)
        elif bucket_type == "log_bucket":
            my_bucket=self.log_bucket(bucket_name)
        else :
             my_bucket=self.data_bucket(bucket_name)


        self.my_bucket=my_bucket

        self.bucket_arn=my_bucket.bucket_arn

    def get_arn(self):
        return bucket_arn

    def add_to_resource_policy(self, PolicyStatment):
        my_bucket.add_to_resource_policy(PolicyStatment)
        
                
    def data_bucket( self,  bucket_name):
        # Import s3 access log bucket 
        bucket_unique_name=bucket_name +  "-" + Aws.ACCOUNT_ID + "-" + Aws.REGION
        access_logs_bucket=s3.Bucket.from_bucket_name(self, "LogBucketImport"+bucket_name, self.log_bucket_name)
        
        #intelegent tiering does not work from here; but the updated transition does same thing. 
        #applying a reaonable work around from https://github.com/aws/aws-cdk/issues/20937#issuecomment-1209515810
        intelligent_tiering_configurations = [s3.IntelligentTieringConfiguration(
            name="AllBucketInteligentPolicy",
            archive_access_tier_time=aws_cdk.Duration.days(90),
            deep_archive_access_tier_time=aws_cdk.Duration.days(180),
            )],
        
        my_bucket=s3.Bucket( self, bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
            bucket_name=bucket_unique_name,
            server_access_logs_bucket=access_logs_bucket,
            server_access_logs_prefix=bucket_unique_name + "/",
            )
    
    
        #with hope of better updatability in the future, splitting off lifecycle rules
        noncurrent_version_transition = s3.NoncurrentVersionTransition(
            storage_class=s3.StorageClass.GLACIER,
            transition_after=aws_cdk.Duration.days(30),
            )
        inelegent_tiering_transition=s3.Transition(
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after=aws_cdk.Duration.days(0),
                )
     
    
        my_bucket.add_lifecycle_rule(
            id="ExpireOldVersions_and_TransitionToIntelegentTiering",
            enabled=True,
            expiration=aws_cdk.Duration.days(365 * 3),
            noncurrent_version_expiration=aws_cdk.Duration.days(365 * 3),
            transitions=[inelegent_tiering_transition],
            noncurrent_version_transitions=[noncurrent_version_transition],
            prefix="",
            tag_filters=None,
        )
        
        #tag the bucket for backup
        aws_cdk.Tags.of(self).add('Backup', 'Default')
        #LZA backup policy - compliant
        aws_cdk.Tags.of(self).add('BackupPlan', 'Daily')
        
        return my_bucket

    def s3_access_log_bucket( self,  bucket_name):
        # Create a bucket with a name
        bucket_unique_name = bucket_name + "-" + Aws.REGION + "-" + Aws.ACCOUNT_ID 
        print(f'bucket={bucket_unique_name}')
        transition = s3.Transition(
            storage_class=s3.StorageClass.GLACIER,
            transition_after=aws_cdk.Duration.days(30),
            )
        my_bucket=s3.Bucket( self, "LogBucket" + bucket_name,
        block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        encryption=s3.BucketEncryption.S3_MANAGED,
        access_control=s3.BucketAccessControl.LOG_DELIVERY_WRITE,
        enforce_ssl=True,
        versioned=False,
        removal_policy=RemovalPolicy.RETAIN,
        bucket_name=bucket_unique_name,
        lifecycle_rules=[
            s3.LifecycleRule(
                transitions=[transition],
                expiration=aws_cdk.Duration.days(365 * 3),
                enabled=True,
                id=f"expiration"
            )
        ],
        )
    
        return my_bucket
    def log_bucket( self,  bucket_name):
        # Create a bucket with a name
        bucket_unique_name = bucket_name + "-" + Aws.REGION + "-" + Aws.ACCOUNT_ID 
        print(f'bucket={bucket_unique_name}')
        transition = s3.Transition(
            storage_class=s3.StorageClass.GLACIER,
            transition_after=aws_cdk.Duration.days(30),
            )
        
        my_bucket=s3.Bucket( self, "LogBucket" + bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=False,
            removal_policy=RemovalPolicy.RETAIN,
            bucket_name=bucket_unique_name,
            lifecycle_rules=[
                s3.LifecycleRule(
                    transitions=[transition],
                    expiration=aws_cdk.Duration.days(365 * 3),
                    enabled=True,
                    id=f"expiration"
                )
            ]
            )
        return my_bucket

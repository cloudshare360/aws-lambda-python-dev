import os
import boto3

# Initialize S3 client (will pick up AWS creds from env or ~/.aws/credentials)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = os.environ.get("BUCKET_NAME")
    if not bucket:
        return {"statusCode": 400, "body": "Environment variable BUCKET_NAME not set"}

    # List objects in the bucket
    resp = s3.list_objects_v2(Bucket=bucket)
    keys = [obj['Key'] for obj in resp.get('Contents', [])]

    return {
        "statusCode": 200,
        "body": {
            "bucket": bucket,
            "objects": keys
        }
    }

import os
from app import lambda_handler

if __name__ == "__main__":
    # 1) Point to a real S3 bucket you own
    os.environ["BUCKET_NAME"] = "my-test-bucket"

    # 2) Mock event & context
    event = {}
    context = {}

    # 3) Invoke
    result = lambda_handler(event, context)
    print("Lambda output:", result)

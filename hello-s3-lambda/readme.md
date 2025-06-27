Below is a complete end-to-end example of a Python Lambda that reads from an S3 bucket, along with instructions on how to test it locally **without** SAM (pure Python), and **with** SAM (using your Codespace environment).

---

## 1️⃣ Folder Structure

```
hello-s3-lambda/
├── app.py
├── test_local.py
├── event.json
└── template.yaml
```

---

## 2️⃣ `app.py` — Lambda Code (List Objects in S3)

```python
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
```

> **Note:** This expects an IAM-authorized set of AWS credentials locally, or a role when deployed.

---

## 3️⃣ `event.json` — Sample Invoke Event

```json
{
  "dummy": "value"
}
```

(Our function ignores the payload and reads the bucket name from an env var.)

---

## 4️⃣ `test_local.py` — Test Without SAM

```python
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
```

### ▶️ Run:

```bash
cd hello-s3-lambda
# ensure your AWS creds are configured in ~/.aws/credentials or env vars:
#   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
python test_local.py
```

You should see something like:

```
Lambda output: {'statusCode': 200, 'body': {'bucket': 'my-test-bucket', 'objects': ['file1.txt', 'dir/file2.png', ...]}}
```

---

## 5️⃣ `template.yaml` — SAM Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Environment:
      Variables:
        BUCKET_NAME: my-test-bucket  # set your bucket here

Resources:
  S3ListFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.12
      CodeUri: .
      Events:
        ProxyApi:
          Type: Api
          Properties:
            Path: /list
            Method: get
```

---

## 6️⃣ Testing **with** SAM Locally

1. **Build** the function:

   ```bash
   cd hello-s3-lambda
   sam build
   ```

2. **Invoke** directly:

   ```bash
   sam local invoke S3ListFunction --event event.json
   ```

3. **Run as API**:

   ```bash
   sam local start-api
   ```

   Then in another shell:

   ```bash
   curl http://localhost:3000/list
   ```

All of these will pick up your `BUCKET_NAME` from the template’s environment variable and your local AWS credentials (make sure `AWS_DEFAULT_REGION` and keys are set).

---

## 7️⃣ Notes on AWS Credentials

* **Credential sources** (in order):

  1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`)
  2. `~/.aws/credentials` and `~/.aws/config`
  3. IAM role if running in AWS

* In GitHub Codespaces you can:

  * Run `aws configure` in the terminal,
  * Or export creds in your Codespace environment,
  * Or use the [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) flow if you wire up federated credentials.

---

That’s it—now you have both a **pure-Python** local test and a **SAM**-backed local API that lists S3 objects. Let me know if you need help mocking S3 (with `moto`) or packaging additional dependencies!

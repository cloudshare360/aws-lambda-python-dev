from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    CfnOutput,
)
from constructs import Construct
import os

class S3CrudStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 1) S3 bucket
        bucket = s3.Bucket(self, "CrudBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # 2) Lambda function
        fn = _lambda.Function(self, "CrudHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda")),
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )
        bucket.grant_read_write(fn)

        # 3) API Gateway REST API
        api = apigateway.RestApi(self, "CrudApi",
            rest_api_name="S3 CRUD Service",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=["GET","PUT","POST","DELETE","OPTIONS"]
            )
        )

        files = api.root.add_resource("files")
        file = files.add_resource("{filename}")

        # proxy all methods to our Lambda
        for m in ["GET","PUT","POST","DELETE"]:
            file.add_method(m, apigateway.LambdaIntegration(fn))

        # 4) Outputs
        CfnOutput(self, "ApiUrl",
            value=api.url + "files/{filename}",
            description="Invoke as: https://.../files/myfile.json"
        )
        CfnOutput(self, "BucketName",
            value=bucket.bucket_name
        )

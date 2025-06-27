#!/usr/bin/env python3
import aws_cdk as cdk
from s3_crud_stack import S3CrudStack

app = cdk.App()
S3CrudStack(app, "S3CrudStack")
app.synth()

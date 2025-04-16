import boto3
import zipfile
import os
import time
from botocore.exceptions import ClientError

LAMBDA_FUNCTION_NAME = "GoInitUpdater"
ZIP_PATH = "lambda.zip"
ROLE_ARN = "arn:aws:iam::000000000000:role/lambda-role"  # فرضی برای localstack

lambda_client = boto3.client(
    "lambda",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

def deploy():
    with open(ZIP_PATH, "rb") as f:
        zipped_code = f.read()

    try:
        lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime="go1.x",
            Role=ROLE_ARN,
            Handler="bootstrap",
            Code={"ZipFile": zipped_code},
            Publish=True,
        )
        print("🚀 Lambda created!")
    except lambda_client.exceptions.ResourceConflictException:
        print("🔁 Lambda exists. Updating...")

        # اینجا یه مکث کوتاه کمک می‌کنه اگر هنوز در حال پردازشه
        time.sleep(2)

        try:
            lambda_client.update_function_code(
                FunctionName=LAMBDA_FUNCTION_NAME,
                ZipFile=zipped_code,
                Publish=True
            )
            print("✅ Lambda updated.")
        except ClientError as e:
            print("❌ Update failed:", e)

if __name__ == "__main__":
    deploy()
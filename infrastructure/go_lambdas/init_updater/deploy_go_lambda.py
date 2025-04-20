import boto3
import zipfile
import os
import time
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

LAMBDA_FUNCTION_NAME = os.getenv('LAMBDA_FUNCTION_NAME')
ZIP_PATH = os.getenv("ZIP_PATH")
ROLE_ARN = os.getenv("ROLE_ARN")

REGION_NAME=os.getenv("REGION_NAME")
AWS_ENDPOINT=os.getenv("AWS_ENDPOINT")
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")



lambda_client = boto3.client(
    "lambda",
    region_name=REGION_NAME,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
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
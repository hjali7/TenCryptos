import boto3
import zipfile
import os
import json
from dotenv import load_dotenv

LAMBDA_FUNCTION_NAME = "TenCryptosLogger"
ZIP_FILE_NAME = "lambda_package.zip"
HANDLER_FILE = "infrastructure/lambda/lambda_handler.py"
ROLE_ARN = "arn:aws:iam::000000000000:role/lambda-role"
LOG_GROUP_NAME = f"/aws/lambda/{LAMBDA_FUNCTION_NAME}"


load_dotenv()

def create_zip():
    with zipfile.ZipFile(ZIP_FILE_NAME, "w") as zipf:
        zipf.write(HANDLER_FILE, arcname="lambda_handler.py")
    print("✅ Lambda code zipped")

def create_log_group():
    logs = boto3.client("logs", region_name=os.getenv("AWS_REGION") , endpoint_url=os.getenv("AWS_ENDPOINT") , aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID") , aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

    try:
        logs.create_log_group(logGroupName=LOG_GROUP_NAME)
        print("📁 Log group created:", LOG_GROUP_NAME)
    except logs.exceptions.ResourceAlreadyExistsException:
        print("⚠️ Log group already exists.")


def deploy_lambda():
    lambda_client = boto3.client(
        "lambda",
        region_name=os.getenv("AWS_REGION"),
        endpoint_url=os.getenv("AWS_ENDPOINT"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    with open(ZIP_FILE_NAME, "rb") as f:
        zipped_code = f.read()

    try:
        lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime="python3.11",
            Role=ROLE_ARN,
            Handler="lambda_handler.handler",
            Code={"ZipFile": zipped_code},
            Publish=True,
        )
        print("🚀 Lambda function created")
    except lambda_client.exceptions.ResourceConflictException:
        lambda_client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME,
            ZipFile=zipped_code,
            Publish=True
        )
        print("🔁 Lambda function updated")

def connect_to_sqs():
    sqs = boto3.client("sqs", endpoint_url="http://localhost:4566")
    queue_url = sqs.get_queue_url(QueueName="tencryptos-queue")["QueueUrl"]

    lambda_client = boto3.client("lambda", endpoint_url="http://localhost:4566")
    lambda_client.create_event_source_mapping(
        EventSourceArn=f"arn:aws:sqs:us-east-1:000000000000:tencryptos-queue",
        FunctionName=LAMBDA_FUNCTION_NAME,
        BatchSize=1
    )
    print("🔗 Lambda connected to SQS queue")

# اجرای کل مراحل
if __name__ == "__main__":
    create_zip()
    create_log_group()
    deploy_lambda()
    connect_to_sqs()

# app/core/aws.py

import boto3
import json
import os
from datetime import datetime

# 🧾 Env
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# 📦 Clients
s3 = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

sqs = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

secretsmanager = boto3.client(
    "secretsmanager",
    endpoint_url=AWS_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# 🔐 Secrets
def get_secret_value(secret_name: str) -> str:
    try:
        response = secretsmanager.get_secret_value(SecretId=secret_name)
        return response["SecretString"]
    except Exception as e:
        print(f"❌ Error fetching secret: {e}")
        return ""

# 📤 S3
def upload_to_s3(data: list[dict]):
    key = f"backup-{datetime.utcnow().isoformat()}.json"
    s3.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=json.dumps(data))
    print(f"📦 [S3] Backup uploaded: {key}")

# 📨 SQS
def send_sqs_message(event: str):
    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps({
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        })
    )
    print("📨 [SQS] Message sent.")

# 📥 SQS
def receive_sqs_message():
    try:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )
        if "Messages" in response:
            message = response["Messages"][0]
            receipt_handle = message["ReceiptHandle"]
            print(f"📥 [SQS] Message received: {message['Body']}")
            sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
        else:
            print("📭 [SQS] No messages to process.")
    except Exception as e:
        print(f"❌ [SQS] Error receiving message: {e}")

# 📃 S3
def list_s3_objects():
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        if "Contents" in response:
            for obj in response["Contents"]:
                print(f"📁 [S3] Object: {obj['Key']}")
        else:
            print("📂 [S3] No objects found.")
    except Exception as e:
        print(f"❌ [S3] Error listing objects: {e}")
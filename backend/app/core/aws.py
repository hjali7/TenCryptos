# app/core/aws.py

import boto3
import json
import os
from datetime import datetime

# 🧾 گرفتن اطلاعات از .env
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# 🔧 ساخت کلاینت‌های S3 و SQS
s3 = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

sqs = boto3.client(
    "sqs",
    endpoint_url=AWS_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# 📤 ارسال بکاپ به S3
def upload_to_s3(data: list[dict]):
    key = f"backup-{datetime.utcnow().isoformat()}.json"
    s3.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=json.dumps(data))
    print(f"📦 [S3] Backup uploaded: {key}")

# 📨 ارسال پیام به SQS
def send_sqs_message(event: str):
    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps({
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        })
    )
    print("📨 [SQS] Message sent.")

# 📥 دریافت پیام از SQS
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

# 📃 لیست اشیاء داخل S3
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
# 🔄 بکاپ‌گیری از دیتابیس
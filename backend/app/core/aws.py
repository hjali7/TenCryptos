# backend/app/core/aws.py
import boto3
import json
from datetime import datetime

# مشخصات اتصال به LocalStack
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

sqs = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

BUCKET_NAME = "tencryptos-backups"
QUEUE_NAME = "tencryptos-queue"
QUEUE_URL = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]

def upload_to_s3(data: list[dict]):
    key = f"backup-{datetime.utcnow().isoformat()}.json"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(data)
    )
    print(f"📦 Backup uploaded to S3: {key}")

def send_sqs_message(event: str):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps({
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        })
    )
    print(f"📨 SQS Message sent: {event}")

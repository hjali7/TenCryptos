import boto3
import json
from datetime import datetime

# استفاده از کانتینر موجود localstack با اسم 'localstack'
s3 = boto3.client(
    "s3",
    endpoint_url="http://localstack:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

sqs = boto3.client(
    "sqs",
    endpoint_url="http://localstack:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

BUCKET_NAME = "tencryptos-backups"
QUEUE_NAME = "tencryptos-queue"


def upload_to_s3(data: list[dict]):
    key = f"backup-{datetime.utcnow().isoformat()}.json"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(data)
    )
    print(f"\ud83d\udce6 [S3] Backup uploaded: {key}")


def get_queue_url():
    return sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]


def send_sqs_message(event: str):
    sqs.send_message(
        QueueUrl=get_queue_url(),
        MessageBody=json.dumps({
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        })
    )
    print("\ud83d\udce9 [SQS] Message sent.")
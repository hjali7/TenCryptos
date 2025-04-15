import boto3
import json
import os


sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

QUEUE_URL= sqs.get_queue_url(QueueName="tencryptos-queue")["QueueUrl"]

def send_event_notification(event_type: str , payload: dist = {}):
    message = {
        "event": event_type,
        "payload": payload,
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message),
    )

    print(f"📬 Event sent to SQS: {event_type}")
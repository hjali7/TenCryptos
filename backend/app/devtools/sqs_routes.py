from fastapi import APIRouter
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SQS_ENDPOINT = os.getenv("AWS_ENDPOINT")
QUEUE_NAME = os.getenv("QUEUE_NAME")

@router.get("/sqs/send")
def send_sqs_message():
    sqs = boto3.client("sqs", endpoint_url=SQS_ENDPOINT)
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
    sqs.send_message(QueueUrl=queue_url, MessageBody="🔥 Devtools test message")
    return {"message": "📤 SQS message sent ✅"}

@router.get("/sqs/receive")
def receive_sqs_message():
    sqs = boto3.client("sqs", endpoint_url=SQS_ENDPOINT)
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    return {"message": "📥 SQS message received ✅", "data": messages.get("Messages", [])}

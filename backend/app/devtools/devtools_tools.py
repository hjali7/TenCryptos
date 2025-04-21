from fastapi import APIRouter
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL")
QUEUE_NAME = os.getenv("QUEUE_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")

@router.get("/s3/list")
def list_s3_objects():
    s3 = boto3.client("s3", endpoint_url=AWS_ENDPOINT)
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    return {"objects": [obj["Key"] for obj in response.get("Contents", [])]}

@router.post("/sqs/send")
def send_sqs_test_message():
    sqs = boto3.client("sqs", endpoint_url=AWS_ENDPOINT)
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
    sqs.send_message(QueueUrl=queue_url, MessageBody='{"event": "🔥 Test event!"}')
    return {"message": "Sent to SQS ✅"}

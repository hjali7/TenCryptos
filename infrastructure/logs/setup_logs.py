import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_ACCESSS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

LOG_GROUP_NAME= os.getenv("LOG_GROUP_NAME")
LOG_STREAM_NAME=os.getenv("LOG_STREAM_NAME")

client = boto3.client(
    "logs",
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESSS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def create_log_group():
    try:
        client.create_log_group(log_group_name=LOG_GROUP_NAME)
        print(f"✅ Created log group: {LOG_GROUP_NAME}")
    except client.exceptions.ResourceAlreadyExistsException:
        print(f"⚠️ Log group already exists: {LOG_GROUP_NAME}")

def create_log_stream():
    try:
        client.create_log_stream(
            log_group_name=LOG_GROUP_NAME,
            log_stream_name=LOG_STREAM_NAME
        )
        print(f"✅ Created log stream: {LOG_STREAM_NAME}")
    except client.exceptions.ResourceAlreadyExistsException:
        print(f"⚠️ Log stream already exists: {LOG_STREAM_NAME}")

if __name__ == "__main__":
    create_log_group()
    create_log_stream()
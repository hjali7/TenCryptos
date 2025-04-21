from fastapi import APIRouter
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

S3_ENDPOINT = os.getenv("AWS_ENDPOINT")
BUCKET_NAME = os.getenv("BUCKET_NAME")

@router.get("/s3/list")
def list_s3_objects():
    s3 = boto3.client("s3", endpoint_url=S3_ENDPOINT)
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    objects = [obj["Key"] for obj in response.get("Contents", [])]
    return {"message": "✅ S3 objects listed", "objects": objects}

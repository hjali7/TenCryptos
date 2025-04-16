# app/routes/devtools.py
from fastapi import APIRouter
from app.core.aws import list_s3_objects, receive_sqs_message, send_sqs_message

router = APIRouter(prefix="/devtools", tags=["DevTools"])

@router.get("/s3/list")
def list_s3():
    try:
        list_s3_objects()
        return {"message": "✅ S3 objects listed (check logs for details)"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/sqs/send")
def send_sqs():
    try:
        send_sqs_message("Test event")
        return {"message": "📨 SQS message sent ✅"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/sqs/receive")
def receive_sqs():
    try:
        receive_sqs_message()
        return {"message": "📥 SQS message received ✅"}
    except Exception as e:
        return {"error": str(e)}

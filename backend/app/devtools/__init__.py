from fastapi import APIRouter
from .sqs_routes import router as sqs_router
from .s3_routes import router as s3_router

router = APIRouter()

router.include_router(sqs_router, prefix="/devtools", tags=["SQS Tools"])
router.include_router(s3_router, prefix="/devtools", tags=["S3 Tools"])

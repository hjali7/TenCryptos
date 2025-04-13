from fastapi import FastAPI
from app.core.database import SessionLocal
from app.services.crypto_service import get_top_10_cryptos
from app.crud.crypto import upsert_cryptos
from app.routes import db_view, logs  # auth موقتاً حذف شد تا رفع ارور
from app.core.logger import logger
from app.core import aws
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

app.include_router(db_view.router)
app.include_router(logs.router)

@app.get("/")
def root():
    return {"message": "TenCryptos backend is alive!"}

@app.post("/cryptos/update")
def update_cryptos():
    logger.info("\ud83d\udce5 [MANUAL SYNC] Started")
    db = SessionLocal()
    try:
        cryptos = [c.dict() for c in get_top_10_cryptos()]
        upsert_cryptos(cryptos, db)
        aws.upload_to_s3(cryptos)
        aws.send_sqs_message("manual_sync")
        logger.info("\u2705 [MANUAL SYNC] Data synced + S3 backup + SQS event")
    except Exception as e:
        logger.error(f"\u274c [ERROR] {e}")
        return {"error": str(e)}
    finally:
        db.close()
        logger.info("\ud83d\udd1a [MANUAL SYNC] DB session closed")
    return {"message": "Manual sync complete with S3 + SQS"}


def scheduled_sync():
    logger.info("\u23f0 [AUTO SYNC] Started")
    db = SessionLocal()
    try:
        cryptos = [c.dict() for c in get_top_10_cryptos()]
        upsert_cryptos(cryptos, db)
        aws.upload_to_s3(cryptos)
        aws.send_sqs_message("auto_sync")
        logger.info("\u2705 [AUTO SYNC] Data synced + S3 backup + SQS event")
    except Exception as e:
        logger.error(f"\u274c [AUTO SYNC ERROR] {e}")
    finally:
        db.close()
        logger.info("\ud83d\udd1a [AUTO SYNC] DB session closed")

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_sync, 'interval', minutes=5)
scheduler.start()

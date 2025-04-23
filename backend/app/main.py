# backend/app/main.py

import os
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import db_view
from app.core.logger import logger
from app.core.database import SessionLocal, Base, engine
from app.devtools import router as devtools_router
from app.devtools import devtools_tools
from app.services.crypto_service import get_top_10_cryptos
from app.crud.crypto import upsert_cryptos
from app.models import db_crypto

# ========================
# 🔐 Load .env and Secrets
# ========================
load_dotenv()

# 🗝️ اگر از Secrets Manager استفاده می‌کنی، اینجا مقداردهی کن
def get_secret_from_aws(secret_name: str) -> str:
    try:
        client = boto3.client(
            service_name='secretsmanager',
            endpoint_url=os.getenv("AWS_ENDPOINT"),
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        response = client.get_secret_value(SecretId=secret_name)
        return response["SecretString"]
    except Exception as e:
        logger.error(f"❌ Failed to load secret '{secret_name}': {e}")
        return None

# ✅ از Secrets Manager بخون و جایگزین کن
db_password_secret = get_secret_from_aws("db-password")
if db_password_secret:
    os.environ["DB_PASSWORD"] = db_password_secret

# ========================
# 🚀 FastAPI Setup
# ========================
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🛡️ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Routers
app.include_router(db_view.router)
app.include_router(devtools_router)
app.include_router(devtools_tools.router, prefix="/devtools-tools")

# ========================
# 🌐 Endpoints
# ========================
@app.get("/")
def root():
    return {"message": "TenCryptos backend is alive!"}

@app.post("/cryptos/update")
def update_cryptos():
    logger.info("📥 [MANUAL SYNC] Started")
    db = SessionLocal()
    try:
        cryptos = [c.dict() for c in get_top_10_cryptos()]
        upsert_cryptos(cryptos, db)
        logger.info("✅ [MANUAL SYNC] Data synced")
        return {"message": "Manual sync complete"}
    except Exception as e:
        logger.error(f"❌ [ERROR] {e}")
        return {"error": str(e)}
    finally:
        db.close()
        logger.info("🔚 [MANUAL SYNC] DB session closed")

@app.get("/cryptos")
def get_cryptos():
    db = SessionLocal()
    try:
        cryptos = db.query(db_crypto.Crypto).all()
        return {"cryptos": [crypto.to_dict() for crypto in cryptos]}
    except Exception as e:
        logger.error(f"❌ [ERROR] {e}")
        return {"error": str(e)}
    finally:
        db.close()
        logger.info("🔚 [GET CRYPTOS] DB session closed")

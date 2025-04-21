# backend/app/main.py

import os
from dotenv import load_dotenv
load_dotenv()
from app.devtools import router as devtools_router
from app.routes import devtools_tools
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import db_view, devtools
from app.core.logger import logger
from app.core.database import SessionLocal, Base, engine
from app.services.crypto_service import get_top_10_cryptos
from app.crud.crypto import upsert_cryptos
from app.models import db_crypto 

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📡 اضافه کردن مسیرها
app.include_router(db_view.router)
app.include_router(devtools.router)
app.include_router(devtools_tools.router, prefix="/devtools-tools")


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
    except Exception as e:
        logger.error(f"❌ [ERROR] {e}")
        return {"error": str(e)}
    finally:
        db.close()
        logger.info("🔚 [MANUAL SYNC] DB session closed")
    return {"message": "Manual sync complete"}

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

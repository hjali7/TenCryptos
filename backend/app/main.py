from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import SessionLocal, Base, engine
from app.services.crypto_service import get_top_10_cryptos
from app.crud.crypto import upsert_cryptos
from app.routes import db_view
from app.core.logger import logger
import os

# 🧱 ساخت جداول به‌صورت خودکار
def create_tables():
    try:
        from app.models import db_crypto  # 👈 اطمینان از ایمپورت مدل‌ها
        Base.metadata.create_all(bind=engine)
        logger.info("🧱 [DB INIT] Tables created")
    except Exception as e:
        logger.error(f"❌ [DB INIT ERROR] {e}")

create_tables()

app = FastAPI()

# 🛡️ فعال‌سازی CORS برای ارتباط با فرانت
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در محیط واقعی دامنه فرانت رو وارد کن
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📡 مسیرها
app.include_router(db_view.router)

@app.get("/")
def root():
    return {"message": "TenCryptos backend is alive!"}

@app.post("/cryptos/update")
def update_cryptos():
    logger.info("📥 [MANUAL SYNC] Started")
    db = SessionLocal()
    try:
        cryptos = [c.model_dump() for c in get_top_10_cryptos()]
        upsert_cryptos(cryptos, db)
        logger.info("✅ [MANUAL SYNC] Data synced")
    except Exception as e:
        logger.error(f"❌ [ERROR] {e}")
        return {"error": str(e)}
    finally:
        db.close()
        logger.info("🔚 [MANUAL SYNC] DB session closed")
    return {"message": "Manual sync complete"}

from fastapi import FastAPI
from app.core.database import SessionLocal
from app.services.crypto_service import get_top_10_cryptos
from app.crud.crypto import upsert_cryptos
from app.routes import db_view, auth

from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# ⬇️ Routerها
app.include_router(db_view.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "TenCryptos backend is alive!"}

@app.post("/cryptos/update")
def update_cryptos():
    print("📥 [MANUAL SYNC] Started")
    db = SessionLocal()
    try:
        cryptos = [c.dict() for c in get_top_10_cryptos()]
        upsert_cryptos(cryptos, db)
        print("✅ [MANUAL SYNC] Data synced")
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return {"error": str(e)}
    finally:
        db.close()
    return {"message": "Manual sync complete"}

# ⏰ تابع sync زمان‌بندی‌شده
def scheduled_sync():
    print("⏰ [AUTO SYNC] Started")
    db = SessionLocal()
    try:
        cryptos = [c.dict() for c in get_top_10_cryptos()]
        upsert_cryptos(cryptos, db)
        print("✅ [AUTO SYNC] Data synced")
    except Exception as e:
        print(f"❌ [AUTO SYNC ERROR] {e}")
    finally:
        db.close()

# 🗓️ Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_sync, 'interval', minutes=5)
scheduler.start()

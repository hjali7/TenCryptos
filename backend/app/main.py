from fastapi import FastAPI
from app.core.database import SessionLocal
from app.services.crypto_service import get_top_10_cryptos
from app.crud.crypto import upsert_cryptos

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TenCryptos backend is alive!"}

@app.post("/cryptos/update")
def update_cryptos():
    print("📥 [INFO] Update started")
    db = SessionLocal()
    try:
        cryptos = [c.dict() for c in get_top_10_cryptos()]
        print("✅ [INFO] Got data from API")
        upsert_cryptos(cryptos, db)
        print("💾 [INFO] Data saved to DB")
    except Exception as e:
        print(f"❌ [ERROR] {e}")
        return {"error": str(e)}
    finally:
        db.close()
        print("🔚 [INFO] DB session closed")
    return {"message": "Data synced to DB"}

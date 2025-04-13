from sqlalchemy.orm import Session
from app.models.db_crypto import CryptoDB

def upsert_cryptos(crypto_list: list[dict], db: Session):
    for crypto in crypto_list:
        existing = db.query(CryptoDB).filter(CryptoDB.symbol == crypto["symbol"]).first()
        if existing:
            existing.price_usd = crypto["price_usd"]
            existing.name = crypto["name"]
        else:
            new = CryptoDB(**crypto)
            db.add(new)
    db.commit()

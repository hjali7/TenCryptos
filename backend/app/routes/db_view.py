from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.core.database import SessionLocal
from app.models.db_crypto import CryptoDB

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cryptos/db")
def get_cryptos_from_db(
    db: Session = Depends(get_db),
    symbol: str = Query(default=None),
    sort_by: str = Query(default="price_usd", regex="^(symbol|name|price_usd)$"),
    order: str = Query(default="desc", regex="^(asc|desc)$"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50)
):
    query = db.query(CryptoDB)

    if symbol:
        query = query.filter(CryptoDB.symbol == symbol.lower())

    # مرتب‌سازی
    sort_column = getattr(CryptoDB, sort_by)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # صفحه‌بندی
    offset = (page - 1) * limit
    cryptos = query.offset(offset).limit(limit).all()

    return [
        {
            "symbol": c.symbol,
            "name": c.name,
            "price_usd": c.price_usd
        }
        for c in cryptos
    ]

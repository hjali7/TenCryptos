from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class CryptoDB(Base):
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    price_usd = Column(Float)

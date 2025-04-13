from pydantic import BaseModel

class Crypto(BaseModel):
    symbol: str
    name: str
    price_usd: float

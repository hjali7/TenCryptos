from fastapi import APIRouter
from app.services.crypto_service import get_top_10_cryptos
from typing import List
from app.models.crypto_model import Crypto

router = APIRouter()

@router.get("/cryptos", response_model=List[Crypto])
def get_cryptos():
    return get_top_10_cryptos()

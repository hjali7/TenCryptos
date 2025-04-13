import requests
from app.models.crypto_model import Crypto

def get_top_10_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    data = response.json()

    return [
        Crypto(
            symbol=coin["symbol"],
            name=coin["name"],
            price_usd=float(coin["current_price"])
        )
        for coin in data
    ]

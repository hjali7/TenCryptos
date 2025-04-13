from fastapi import FastAPI
from app.routes import crypto

app = FastAPI()

app.include_router(crypto.router)

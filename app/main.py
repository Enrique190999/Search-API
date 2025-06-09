# app/main.py
from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Search-API")

app.include_router(router)

from fastapi import APIRouter
from .sys import router as sys

api_router = APIRouter(prefix="/api")  # Prefix utama untuk semua route API

# Tambahkan sub-router
api_router.include_router(sys)
from fastapi import APIRouter
from .sys import router as sys
from .debug import router as debug
from .docker import router as docker

api_router = APIRouter(prefix="/api")  # Prefix utama untuk semua route API

# Tambahkan sub-router
api_router.include_router(debug)
api_router.include_router(sys)
api_router.include_router(docker)

from fastapi import APIRouter
from .sys import router as sys
from .debug import router as debug
from .docker import router as docker
from .shortcut_app import router as shortcut_app
from .category_app import router as category_app

api_router = APIRouter(prefix="/api")  # Prefix utama untuk semua route API

# Tambahkan sub-router
api_router.include_router(debug)
api_router.include_router(sys)
api_router.include_router(docker)
api_router.include_router(shortcut_app)
api_router.include_router(category_app)

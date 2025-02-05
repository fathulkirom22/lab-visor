from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from app.database import test_connection
from app.responses import BaseResponse, ErrorResponse
from app.routers import sys, admin

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(sys.router)
app.include_router(admin.router)

@app.get("/", response_model=Union[BaseResponse, ErrorResponse])
def get_root() -> BaseResponse | ErrorResponse:
    try:
        data = test_connection()
        return BaseResponse(message=data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )


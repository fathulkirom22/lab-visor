from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from .routers import home
from .routers.api import api_router
from .startup import lifespan

app = FastAPI(lifespan=lifespan)

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

# @app.middleware("http")
# async def error_handling_middleware(request: Request, call_next):
#     try:
#         response = await call_next(request)
#         return response
#     except Exception as e:
#         return HTMLResponse(status_code=500, content=f"Error: {str(e)}")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)
app.include_router(home.router)

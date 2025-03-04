from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from .routers import home, sys, container
from .routers.api import api_router
from .startup import lifespan

app = FastAPI(lifespan=lifespan)

origins = ["*"]

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

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)
app.include_router(home.router)
app.include_router(sys.router)
app.include_router(container.router)


@app.exception_handler(404)
async def custom_404_handler(request, __):
    """404 error handler"""
    return templates.TemplateResponse("404.jinja", {"request": request})

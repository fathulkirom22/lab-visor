from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.utils import minify_html

router = APIRouter(
    tags=["home"],
    responses={404: {"description": "Not found"}},
    include_in_schema=False
)

templates = Jinja2Templates(directory="app/templates")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True

@router.get("/")
async def view_root(request: Request):
    res = templates.TemplateResponse("home/index.jinja", {"request": request, "title": "Home Dashboard"})
    minify = await minify_html(res)
    return minify

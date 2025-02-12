from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.utils import minify_html

html = str

router = APIRouter(
    prefix="/sys",
    tags=["sys"],
    include_in_schema=False
)

templates = Jinja2Templates(directory="app/templates")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True

@router.get("/")
async def view_root(request: Request):
    _tamplate = "sys/index.jinja"
    res = templates.TemplateResponse(_tamplate, {"request": request, "title": "System Info"})
    minify = await minify_html(res)
    return minify
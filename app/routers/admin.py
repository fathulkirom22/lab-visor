from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    include_in_schema=False
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def view_root(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request, "title": "Admin Dashboard"})
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.utils import minify_html
from app.database import SessionDep
from fastapi import Form
from typing import Annotated
from app.models import ShortcutApp
from app.request import ShortcutAppCreate
from sqlmodel import select

html = str

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
    _tamplate = "home/index.jinja"
    res = templates.TemplateResponse(_tamplate, {"request": request, "title": "Home Dashboard"})
    minify = await minify_html(res)
    return minify

@router.post("/shortcut-app/save", response_class=HTMLResponse)
async def post_shortcut_app(
    db: SessionDep,
    item: Annotated[ShortcutAppCreate, Form()]
):
    _tamplate = "alert.jinja"
    _item = ShortcutApp(**item.model_dump())
    if _item.id:
        existing_item = db.get(ShortcutApp, _item.id)
        
        if existing_item:
            existing_item.sqlmodel_update(_item)
            _item = existing_item
        else:
            raise HTTPException(status_code=404, detail="Shortcut app not found")

    db.add(_item)
    db.commit()
    db.refresh(_item) 
    ctx = {"message": "Success save shortcut !", "variant": "success"}
    html_content: html = templates.get_template(_tamplate).render(ctx)
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/shortcut-app/list", response_class=HTMLResponse)
async def get_list_shortcut_app(
    db: SessionDep
):
    def card(item: ShortcutApp):
        _tamplate = "home/card-shortcut-app.jinja"
        res = templates.get_template(_tamplate).render({"item": item})
        return res

    data = db.exec(select(ShortcutApp)).all()
    html_content: html = f"""
        <div class="row">
            {''.join(map(card, data))}
        </div>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router.delete("/shortcut-app/{_id}", response_class=HTMLResponse)
def delete_shortcut_app(
    _id: int,
    db: SessionDep
):
    _tamplate = "alert.jinja"
    _item = db.get(ShortcutApp, _id)
    if not _item:
        raise HTTPException(status_code=404, detail="Shortcut not found")
    db.delete(_item)
    db.commit()
    ctx = {"message": "Success delete shortcut !", "variant": "danger"}
    html_content: html = templates.get_template(_tamplate).render(ctx)
    return HTMLResponse(content=html_content, status_code=200)

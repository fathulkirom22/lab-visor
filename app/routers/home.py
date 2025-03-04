from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, Query, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import select, update, func
from app.utils import minify_html
from app.models import ShortcutApp, CategoryApp
from app.database import SessionDep
from app.request import ShortcutAppCreate, CategoryAppCreate
from app.responses import ToastResponse

html = str

router = APIRouter(tags=["home"], include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True


@router.get("/")
async def view_root(
    request: Request,
    page_edit: Annotated[int, Query(ge=0, le=1)] = 0,
) -> HTMLResponse:
    _tamplate = "home/index.jinja"

    res = templates.TemplateResponse(
        _tamplate,
        {"request": request, "title": "Home Dashboard", "page_edit": page_edit},
    )
    minify = await minify_html(res)
    return minify


@router.post("/shortcut-app/save", response_model=ToastResponse)
async def post_shortcut_app(
    db: SessionDep, item: Annotated[ShortcutAppCreate, Form()]
) -> ToastResponse:
    _item = ShortcutApp(**item.model_dump())
    _item.icon = _item.icon.lower()
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
    return ToastResponse(message=f"Success save {_item.name} shortcut !")


@router.get("/shortcut-app/list", response_class=HTMLResponse)
async def get_list_shortcut_app(db: SessionDep):
    def card(item: ShortcutApp):
        _tamplate = "home/card-shortcut-app.jinja"
        res = templates.get_template(_tamplate).render({"item": item})
        return res

    data = db.exec(
        select(ShortcutApp)
        .where(ShortcutApp.category_app_id == None)
        .join(CategoryApp, ShortcutApp.category_app_id == CategoryApp.id)
    ).all()
    if len(data) <= 0:
        html_content: html = (
            """<h1 class="text-center"><i class="bi bi-exclamation-diamond"></i></h1>"""
        )
        return HTMLResponse(content=html_content, status_code=200)

    html_content: html = f"""<div class="row">{''.join(map(card, data))}</div>"""
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/shortcut-app/list/{_id_category}", response_class=HTMLResponse)
async def get_list_shortcut_app_by_id(
    db: SessionDep,
    _id_category: int,
    page_edit: Annotated[int, Query(ge=0, le=1)] = 0,
):
    def card(item: ShortcutApp):
        _tamplate = "home/card-shortcut-app.jinja"
        res = templates.get_template(_tamplate).render(
            {"item": item, "page_edit": page_edit}
        )
        return res

    data = db.exec(
        select(ShortcutApp).where(ShortcutApp.category_app_id == _id_category)
    ).all()
    if len(data) <= 0:
        html_content: html = (
            """<h1 class="text-center"><i class="bi bi-exclamation-diamond"></i></h1>"""
        )
        return HTMLResponse(content=html_content, status_code=200)

    html_content: html = f"""<div class="row">{''.join(map(card, data))}</div>"""
    return HTMLResponse(content=html_content, status_code=200)


@router.delete("/shortcut-app/{_id}", response_model=ToastResponse)
def delete_shortcut_app(_id: int, db: SessionDep) -> ToastResponse:
    _item = db.get(ShortcutApp, _id)
    if not _item:
        raise HTTPException(status_code=404, detail="Shortcut not found")
    db.delete(_item)
    db.commit()
    return ToastResponse(
        message=f"Success delete shortcut {_item.name} !", variant="info"
    )


@router.post("/category-app/save", response_model=ToastResponse)
async def post_category_app(
    db: SessionDep, item: Annotated[CategoryAppCreate, Form()]
) -> ToastResponse:
    _item = CategoryApp(**item.model_dump())
    _item.icon = _item.icon.lower()

    if _item.order:
        db.exec(
            update(CategoryApp)
            .where(CategoryApp.order >= _item.order, CategoryApp.order < 99)
            .values(order=CategoryApp.order + 1)
        )

    if _item.id:
        existing_item = db.get(CategoryApp, _item.id)

        if existing_item:
            existing_item.sqlmodel_update(_item)
            _item = existing_item
        else:
            raise HTTPException(status_code=404, detail="Category app not found")

    db.add(_item)
    db.commit()
    db.refresh(_item)
    return ToastResponse(message=f"Success save {_item.name} category !")


@router.get("/category-app/list", response_class=HTMLResponse)
async def get_list_category_app(
    db: SessionDep,
    page_edit: Annotated[int, Query(ge=0, le=1)] = 0,
) -> HTMLResponse:

    def card(item: CategoryApp):
        _tamplate = "home/card-category-app.jinja"
        res = templates.get_template(_tamplate).render(
            {"item": item, "page_edit": page_edit}
        )
        return res

    data = db.exec(select(CategoryApp).order_by(CategoryApp.order)).all()
    if len(data) <= 0:
        html_content: html = (
            """<h1 class="text-center"><i class="bi bi-exclamation-diamond"></i></h1>"""
        )
        return HTMLResponse(content=html_content, status_code=200)

    html_content: html = f"""<div>{''.join(map(card, data))}</div>"""
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/category-app/list/options", response_class=HTMLResponse)
async def get_options_category_app(
    db: SessionDep, default: Annotated[str, Query()] = ""
):
    def card(item: CategoryApp):
        id_default = None if not default else int(default)
        selected = "selected" if item.id == id_default else ""
        html_content: html = (
            f"""<option value="{item.id}" {selected}>{item.name}</option>"""
        )
        return html_content

    data = db.exec(select(CategoryApp)).all()
    if len(data) <= 0:
        html_content: html = (
            """<h1 class="text-center"><i class="bi bi-exclamation-diamond"></i></h1>"""
        )
        return HTMLResponse(content=html_content, status_code=200)

    html_content: html = "".join(map(card, data))
    return HTMLResponse(content=html_content, status_code=200)


@router.delete("/category-app/{_id}", response_model=ToastResponse)
def delete_category_app(_id: int, db: SessionDep) -> ToastResponse:
    _apps = db.exec(select(ShortcutApp).where(ShortcutApp.category_app_id == _id)).all()

    if len(_apps):
        raise HTTPException(status_code=400, detail="Category not empty!")

    _item = db.get(CategoryApp, _id)
    if not _item:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(_item)
    db.commit()
    return ToastResponse(
        message=f"Success delete category {_item.name} !", variant="info"
    )


@router.get("/category-app/order/options", response_class=HTMLResponse)
async def get_order_options_category_app(
    db: SessionDep, default: Annotated[str, Query()] = ""
):
    def card(item: int, total: int):
        value = item + 1
        id_default = total if not default else int(default)
        selected = "selected" if value == id_default else ""
        html_content: html = f"""<option value="{value}" {selected}>{value}</option>"""
        return html_content

    total = db.exec(
        select(func.count()).select_from(CategoryApp)
    ).one()  # pylint: disable=not-callable

    if not default:
        total += 1

    html_content: html = "<option value='99'>-</option>" + "".join(
        map(lambda x: card(x, total), range(total))
    )
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/category-app/theme/options", response_class=HTMLResponse)
async def get_theme_options_category_app(default: Annotated[str, Query()] = ""):
    THEMES = [
        "primary",
        "secondary",
        "tertiary",
        "success",
        "danger",
        "warning",
        "info",
    ]

    def card(item: str):
        selected = "selected" if item == default else ""
        html_content: html = (
            f"""<option value="{item}" {selected}>{item.title()}</option>"""
        )
        return html_content

    html_content: html = "".join(map(card, THEMES))
    return HTMLResponse(content=html_content, status_code=200)

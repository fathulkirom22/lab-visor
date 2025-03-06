from typing import Annotated
from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.utils import minify_html
import docker
from fastapi import HTTPException
from app.utils import get_docker_client

html = str

router = APIRouter(prefix="/container", tags=["container"], include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True


@router.get("/")
async def view_root_container(
    request: Request,
) -> HTMLResponse:
    _tamplate = "container/index.jinja"

    res = templates.TemplateResponse(
        _tamplate,
        {"request": request, "title": "Container"},
    )
    minify = await minify_html(res)
    return minify


@router.get("/list")
async def get_list_container(
    request: Request,
) -> HTMLResponse:
    def card(item):
        _tamplate = "container/card-container.jinja"
        res = templates.get_template(_tamplate).render(
            {"request": request, "item": item}
        )
        return res

    client = get_docker_client()
    containers = client.containers.list(all=True)

    if len(containers) <= 0:
        _tamplate = "empty.jinja"
        html_content = templates.get_template(_tamplate).render()
        return HTMLResponse(content=html_content, status_code=200)

    html_content: html = f"""<div class="row">{''.join(map(card, containers))}</div>"""
    return HTMLResponse(content=html_content, status_code=200)

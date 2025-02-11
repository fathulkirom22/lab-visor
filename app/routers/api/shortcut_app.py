from typing import Literal, Annotated

from fastapi import HTTPException, Query, APIRouter, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc
from sqlmodel import select, func
from app.models import ShortcutApp
from app.database import SessionDep
from app.responses import ErrorResponse, PaginatedResponse, BaseResponse
from app.request import ShortcutAppCreate

router = APIRouter(
    prefix="/shortcut-app",
    tags=["shortcut-app"],
    responses={404: {"description": "Not found"}},
)
      
@router.get("/", response_model=PaginatedResponse)
async def get_list_shortcut_app(
    db: SessionDep,
    sort_by: Annotated[Literal["id", "name", "link", "icon", "description", "created_at"], Query()] = "created_at",
    order: Annotated[Literal["asc", "desc"], Query()] = "asc",
    direction: Annotated[Literal["asc", "desc"], Query()] = "asc",
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10
):
    column = getattr(ShortcutApp, sort_by, None)
    if not column:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message="Invalid sorting column"))
        )
    
    sort_order = asc(column) if order.lower() == "asc" else desc(column)
    total = db.exec(select(func.count()).select_from(ShortcutApp)).one()
    total_pages = (total + size - 1) // size
    data = db.exec(select(ShortcutApp).order_by(sort_order).offset((page - 1) * size).limit(size)).all()
    if direction == "desc":
        data = data[::-1]
    return PaginatedResponse(
        page=page,
        size=size,
        total=total,
        total_pages=total_pages,
        data=jsonable_encoder(data)
    )

@router.post("/", response_model=BaseResponse)
async def post_shortcut_app(
    db: SessionDep,
    item: Annotated[ShortcutAppCreate, Form()]
):
    db_item = ShortcutApp(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  
    return BaseResponse(
        data=jsonable_encoder(db_item)
    )

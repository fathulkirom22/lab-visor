from typing import Union, Literal, Annotated

from fastapi import Depends, HTTPException, Query, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models import SysDataTracker
from app.database import get_db
from app.responses import ErrorResponse, SysDataTrackerResponse

router = APIRouter(
    prefix="/sys",
    tags=["sys"],
    responses={404: {"description": "Not found"}},
)

@router.get("/data-tracker", response_model=Union[SysDataTrackerResponse, ErrorResponse])
async def get_sys_data_tracker(
    db: Session = Depends(get_db),
    sort_by: Annotated[Literal["id", "cpu", "memory", "quota", "created_at", "quota_response", "ERROR"], Query()] = "created_at",
    order: Annotated[Literal["asc", "desc"], Query()] = "desc",
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10
) -> SysDataTrackerResponse | ErrorResponse:
    try:
        column = getattr(SysDataTracker, sort_by, None)
        if not column:
            raise Exception("Invalid sorting column")
        
        sort_order = asc(column) if order.lower() == "asc" else desc(column)
        total = db.query(SysDataTracker).count()
        total_pages = (total + size - 1) // size
        data = db.query(SysDataTracker).order_by(sort_order).offset((page - 1) * size).limit(size).all()
        return SysDataTrackerResponse(
            page=page,
            size=size,
            total=total,
            total_pages=total_pages,
            data=jsonable_encoder(data)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )

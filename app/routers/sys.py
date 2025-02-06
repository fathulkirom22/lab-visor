from typing import Union, Literal, Annotated

from fastapi import Depends, HTTPException, Query, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models import SysDataTracker
from app.database import get_db
from app.responses import ErrorResponse, SysDataTrackerResponse, BaseResponse
import requests

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

@router.get("/uptime", response_model=Union[BaseResponse, ErrorResponse])
def get_sys_uptime():
    try:    
        with open('/proc/uptime') as f: uptime = float(f.read().split()[0])
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        return BaseResponse(data={"hours": hours, "minutes": minutes, "text":f"{hours} hours {minutes} minutes"})
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )
    
@router.get("/info", response_model=Union[BaseResponse, ErrorResponse])
def get_sys_uptime():
    try:    
        response = requests.get('http+unix://%2Fvar%2Frun%2Fdocker.sock/info')
        data = response.json()
        return BaseResponse(data=data)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )
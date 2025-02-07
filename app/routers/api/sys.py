from typing import Union, Literal, Annotated

from fastapi import Depends, HTTPException, Query, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlmodel import select, func
from sqlalchemy import asc, desc
from app.models import SysDataTracker
from app.database import SessionDep
from app.responses import ErrorResponse, SysDataTrackerResponse, BaseResponse
# from app.database import test_connection
import docker
import psutil
from datetime import datetime

docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

router = APIRouter(
    prefix="/sys",
    tags=["sys"],
    responses={404: {"description": "Not found"}},
)

# @router.get("/health-check", response_model=Union[BaseResponse, ErrorResponse])
# def get_sys_health_check() -> BaseResponse | ErrorResponse:
#     try:
#         data = test_connection()
#         return BaseResponse(message=data)
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=jsonable_encoder(ErrorResponse(message=str(e)))
#         )
    
@router.get("/data-tracker", response_model=Union[SysDataTrackerResponse, ErrorResponse])
async def get_sys_data_tracker(
    db: SessionDep,
    sort_by: Annotated[Literal["id", "cpu", "memory", "quota", "created_at", "quota_response", "ERROR"], Query()] = "created_at",
    order: Annotated[Literal["asc", "desc"], Query()] = "desc",
    direction: Annotated[Literal["asc", "desc"], Query()] = "desc",
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10
) -> SysDataTrackerResponse | ErrorResponse:
    try:
        column = getattr(SysDataTracker, sort_by, None)
        if not column:
            raise Exception("Invalid sorting column")
        
        sort_order = asc(column) if order.lower() == "asc" else desc(column)
        total = db.exec(select(func.count()).select_from(SysDataTracker)).one()
        total_pages = (total + size - 1) // size
        data = db.exec(select(SysDataTracker).order_by(sort_order).offset((page - 1) * size).limit(size)).all()
        if direction == "desc":
            data = data[::-1]
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
        data = docker_client.info()
        return BaseResponse(data=data)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )
    
@router.get("/disk", response_model=Union[BaseResponse, ErrorResponse])
def get_sys_disk():
    try:
        response = psutil.disk_usage('/')
        data = {
            "total": response.total,
            "used": response.used,
            "free": response.free,
            "percent_used": response.percent
        }
        return BaseResponse(data=data)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )

@router.get("/cpu-usage", response_model=Union[BaseResponse, ErrorResponse])
def get_sys_cpu_usage():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)  # Perbarui setiap detik
        data = {
            "cpu_percent": cpu_percent,
            "datetime": datetime.now().isoformat()
        }
        return BaseResponse(data=data)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )
    
@router.get("/memory-usage", response_model=Union[BaseResponse, ErrorResponse])
def get_sys_memory_usage():
    try:
        response = psutil.virtual_memory()
        data = {
            "total": response.total,
            "available": response.available,
            "used": response.used,
            "percent_used": response.percent,
            "datetime": datetime.now().isoformat()
        }
        return BaseResponse(data=data)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=jsonable_encoder(ErrorResponse(message=str(e)))
        )

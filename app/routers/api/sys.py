from typing import Literal, Annotated
from datetime import datetime
import psutil
import os

from fastapi import HTTPException, Query, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc
from sqlmodel import select, func
from app.models import SysDataTracker
from app.database import SessionDep
from app.responses import ErrorResponse, SysDataTrackerResponse, BaseResponse
from app.utils import convert_bytes

router = APIRouter(
    prefix="/sys",
    tags=["sys"],
    responses={404: {"description": "Not found"}},
)


@router.get("/data-tracker", response_model=BaseResponse)
async def get_sys_data_tracker(
    db: SessionDep,
    sort_by: Annotated[
        Literal[
            "id", "cpu", "memory", "quota", "created_at", "quota_response", "ERROR"
        ],
        Query(),
    ] = "created_at",
    order: Annotated[Literal["asc", "desc"], Query()] = "desc",
    direction: Annotated[Literal["asc", "desc"], Query()] = "desc",
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
) -> SysDataTrackerResponse:
    column = getattr(SysDataTracker, sort_by, None)
    if not column:
        raise HTTPException(
            status_code=500,
            detail=jsonable_encoder(ErrorResponse(message="Invalid sorting column")),
        )

    sort_order = asc(column) if order.lower() == "asc" else desc(column)
    total = db.exec(
        select(func.count()).select_from(SysDataTracker)  # pylint: disable=not-callable
    ).one()
    total_pages = (total + size - 1) // size
    data = db.exec(
        select(SysDataTracker)
        .order_by(sort_order)
        .offset((page - 1) * size)
        .limit(size)
    ).all()
    if direction == "desc":
        data = data[::-1]
    return SysDataTrackerResponse(
        page=page,
        size=size,
        total=total,
        total_pages=total_pages,
        data=jsonable_encoder(data),
    )


@router.get("/uptime", response_model=BaseResponse)
def get_sys_uptime() -> BaseResponse:
    with open("/proc/uptime") as f:
        uptime = float(f.read().split()[0])
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    return BaseResponse(
        data={
            "hours": hours,
            "minutes": minutes,
            "text": f"{hours} hours {minutes} minutes",
        }
    )


@router.get("/disk", response_model=BaseResponse)
def get_sys_disk() -> BaseResponse:
    response = psutil.disk_usage("/")
    data = {
        "total": response.total,
        "used": response.used,
        "free": response.free,
        "percent_used": response.percent,
    }
    return BaseResponse(data=data)


@router.get("/cpu-usage", response_model=BaseResponse)
def get_sys_cpu_usage() -> BaseResponse:
    cpu_percent = psutil.cpu_percent(interval=1)  # Perbarui setiap detik
    data = {"cpu_percent": cpu_percent, "datetime": datetime.now().isoformat()}
    return BaseResponse(data=data)


@router.get("/memory-usage", response_model=BaseResponse)
def get_sys_memory_usage() -> BaseResponse:
    response = psutil.virtual_memory()
    data = {
        "total": convert_bytes(response.total),
        "available": response.available,
        "used": response.used,
        "percent_used": response.percent,
        "datetime": datetime.now().isoformat(),
    }
    return BaseResponse(data=data)


@router.get("/info", response_model=BaseResponse)
def get_sys_info() -> BaseResponse:
    _os = os.uname()
    _ncpu = os.cpu_count()
    data = {
        "os": f"{_os.sysname} - {_os.release}",
        "architecture": _os.machine,
        "nodename": _os.nodename,
        "version": _os.version,
        "ncpu": _ncpu,
    }
    return BaseResponse(data=data)

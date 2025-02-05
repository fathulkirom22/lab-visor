from typing import Union, Any, Optional

from pydantic import BaseModel
from datetime import datetime

class ItemSysDataTracker(BaseModel):
    id: int
    cpu: float
    memory: float
    quota: Union[float, None] = None
    created_at: datetime
    quota_response: Any

class BaseResponse(BaseModel):
    status: str = "success"
    message: str = "OK"
    data: Optional[Any] = None

class ErrorResponse(BaseResponse):
    status: str = "error"
    data: None = None

class PaginatedResponse(BaseResponse):
    page: int
    size: int
    total: int
    total_pages: int
    data: list[dict]

class SysDataTrackerResponse(PaginatedResponse):
    data: list[ItemSysDataTracker]
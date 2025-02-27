from fastapi import APIRouter
from app.database import test_connection
from app.responses import BaseResponse

router = APIRouter(
    prefix="/debug",
    tags=["debug"],
    responses={404: {"description": "Not found"}},
)


@router.get("/error")
async def get_error():
    result = 10 / 0
    return {"items": result}


@router.get("/health-check", response_model=BaseResponse)
def get_health_check() -> BaseResponse:
    data = test_connection()
    return BaseResponse(message=data)

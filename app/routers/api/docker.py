from fastapi import APIRouter, HTTPException
from app.responses import BaseResponse
import docker
from app.utils import get_docker_client

router = APIRouter(prefix="/docker", tags=["docker"])


@router.get("/info", response_model=BaseResponse)
def get_docker_info() -> BaseResponse:
    client = get_docker_client()
    return BaseResponse(data=client.info())

from fastapi import APIRouter, HTTPException
from app.responses import BaseResponse
import docker

router = APIRouter(prefix="/docker", tags=["docker"])


def get_docker_client():
    try:
        client = docker.from_env()
        client.ping()
        return client
    except Exception:
        raise HTTPException(status_code=503, detail="Docker service unavailable")


@router.get("/info", response_model=BaseResponse)
def get_docker_info() -> BaseResponse:
    client = get_docker_client()
    return BaseResponse(data=client.info())

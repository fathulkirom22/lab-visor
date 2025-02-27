from fastapi import APIRouter
from app.responses import BaseResponse
import docker

docker_client = docker.DockerClient(base_url="unix://var/run/docker.sock")

router = APIRouter(
    prefix="/docker",
    tags=["docker"],
    responses={404: {"description": "Not found"}},
)


@router.get("/info", response_model=BaseResponse)
def get_docker_info() -> BaseResponse:
    data = docker_client.info()
    return BaseResponse(data=data)

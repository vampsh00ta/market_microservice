from fastapi import APIRouter, Depends,Response
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.grpc_server.grpc_client import grpc_client

router = APIRouter(
    prefix = "/recommendations",
    tags = ["recommendations"]
)


@router.get('/')
async def get_recommendations(request:Request,jwt:str):
    user_id = grpc_client.get_user_data(jwt)
    return {'user_id':user_id.id}

from fastapi import APIRouter, status

from src.apis.accounts import auth
from src.schema import response


auth_router = APIRouter(tags=["auth"])

auth_router.add_api_route(
    methods=["POST"],
    path="/signup",
    endpoint=auth.user_sign_up_handler,
    response_model=response.JWTResponse,
    status_code=status.HTTP_201_CREATED,
)
auth_router.add_api_route(
    methods=["POST"],
    path="/login",
    endpoint=auth.user_login_handler,
    response_model=response.JWTResponse,
    status_code=status.HTTP_200_OK,
)
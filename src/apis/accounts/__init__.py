from fastapi import APIRouter, status

from src.apis.accounts import auth, profile
from src.schema import response

account_router = APIRouter(tags=["auth"], prefix="/account")

account_router.add_api_route(
    methods=["POST"],
    path="/signup",
    endpoint=auth.user_sign_up_handler,
    response_model=response.JWTResponse,
    status_code=status.HTTP_201_CREATED,
)
account_router.add_api_route(
    methods=["POST"],
    path="/login",
    endpoint=auth.user_login_handler,
    response_model=response.JWTResponse,
    status_code=status.HTTP_200_OK,
)
account_router.add_api_route(
    methods=["POST"],
    path="/profile",
    endpoint=profile.profile_create_handler,
    response_model=response.CreateProfileResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["GET"],
    path="/profiles",
    endpoint=profile.profile_lists_handler,
    response_model=list[response.GetProfileResponse],
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["GET"],
    path="/profiles/{profile_id}",
    endpoint=profile.profile_handler,
    response_model=response.GetProfileResponse,
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["PATCH"],
    path="/profile",
    endpoint=profile.update_profile_handler,
    response_model=response.CreateProfileResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["DELETE"],
    path="/profiles/{profile_id}",
    endpoint=profile.delete_profile_handler,
    response_model=response.CreateProfileResponse,
    status_code=status.HTTP_200_OK
)
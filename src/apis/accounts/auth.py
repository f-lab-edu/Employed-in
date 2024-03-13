from fastapi import APIRouter, Depends, HTTPException

from src.models.accounts import User
from src.models.repository import UserRepository
from src.schema.request import SignUpRequest, LoginRequest
from src.schema.response import JWTResponse
from src.service.accounts import UserService


router = APIRouter(prefix="/Accounts")


@router.post("/sign_up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends()
):
    hashed_password: str = user_service.hash_password(
        plain_password=request.password
    )
    user: User = User.create(
        email=request.email,
        password=hashed_password,
        nickname=request.nickname,
        membership_id=request.membership_id
    )
    user: User = user_repo.create_user(user=user)
    token: str = user_service.create_jwt(user.email)

    return JWTResponse(access_token=token)


@router.post("/login", status_code=200)
def user_login_handler(
        request: LoginRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends()
):
    user: User | None = user_repo.get_user_by_email(request.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    verify: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password
    )

    if not verify:
        raise HTTPException(status_code=401, detail="Invalid password")

    token: str = user_service.create_jwt(user_email=user.email)

    return JWTResponse(access_token=token)

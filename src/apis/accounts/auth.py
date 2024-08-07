from fastapi import Depends, HTTPException

from src.models.accounts import User
from src.models.repository import AccountRepository
from src.schema.request import LoginRequest, SignUpRequest
from src.schema.response import JWTResponse
from src.service.accounts import UserService


async def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: AccountRepository = Depends(),
):
    if await user_repo.get_user_by_email(user_email=request.email):
        raise HTTPException(status_code=400, detail="already registered")

    hashed_password: str = user_service.hash_password(plain_password=request.password)
    user: User = User(
        email=request.email,
        password=hashed_password,
        nickname=request.nickname,
        phone_number=request.phone_number,
        is_business=request.is_business,
        is_admin=False,
        membership_id=request.membership_id,
    )
    user: User = await user_repo.add_object(obj=user)
    token: str = user_service.create_jwt(user.email)

    return JWTResponse(access_token=token)


async def user_login_handler(
    request: LoginRequest,
    user_service: UserService = Depends(),
    user_repo: AccountRepository = Depends(),
):
    user: User | None = await user_repo.get_user_by_email(request.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    verify: bool = user_service.verify_password(
        plain_password=request.password, hashed_password=user.password
    )

    if not verify:
        raise HTTPException(status_code=401, detail="Invalid password")

    token: str = user_service.create_jwt(user_email=user.email)

    return JWTResponse(access_token=token)

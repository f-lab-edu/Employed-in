from fastapi import HTTPException, Header, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.profile import Profile
from src.models.accounts import User
from src.service.accounts import UserService
from src.models.repository import ProfileRepository, UserRepository
from src.schema.request import CreateProfileRequest
from src.schema.response import CreateProfileResponse
from src.lib.permission import basic_authentication, get_access_token


def profile_create_handler(
    request: CreateProfileRequest,
    token: str = Depends(get_access_token),
    user_repo: UserRepository = Depends(),
    profile_repo: ProfileRepository = Depends()
    ):

    #user_email = user_service.decode_jwt(access_token=Header("Authorization"))
    #user = user_repo.get_user_by_email(user_email)
    user: User = basic_authentication(token=token, user_repo=user_repo)

    new_profile: Profile = Profile(
        name=request.name,
        occupation=request.occupation,
        personal_description=request.personal_description,
        region=request.region,
        country_id=request.country_id,
        user_id=user.id
    )
    profile: Profile = profile_repo.create_profile(new_profile)

    return CreateProfileResponse(message="New profile created", data=profile)

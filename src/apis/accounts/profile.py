from fastapi import HTTPException, Header, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.profile import Profile, Country
from src.models.accounts import User
from src.service.accounts import UserService
from src.models.repository import ProfileRepository, UserRepository
from src.schema.request import CreateProfileRequest
from src.schema.response import CreateProfileResponse, GetProfileResponse
from src.interfaces.permission import basic_authentication, get_access_token


def profile_create_handler(
    request: CreateProfileRequest,
    token: str = Depends(get_access_token),
    user_repo: UserRepository = Depends(),
    profile_repo: ProfileRepository = Depends()
    ):

    user: User = basic_authentication(token=token, user_repo=user_repo)

    if not profile_repo.profile_validation(user_id=user.id, country_id=request.country_id):
        raise HTTPException(status_code=400, detail="Profile for that country exists")

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


def profile_lists_handler(
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        profile_repo: ProfileRepository = Depends()
):
    user: User = basic_authentication(token=token, user_repo=user_repo)

    profiles: list[(Profile, Country)] = profile_repo.filter_profile_by_user(user_id=user.id)

    return sorted(
        [
            GetProfileResponse(
                id=profile.id,
                name=profile.name,
                occupation=profile.occupation,
                personal_description=profile.personal_description,
                region=profile.region,
                country_name=country
            )
            for profile, country in profiles
        ],
        key=lambda profile: -profile.id,
    )


def profile_handler(
        profile_id: int,
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        profile_repo: ProfileRepository = Depends(),
):
    user: User = basic_authentication(token=token, user_repo=user_repo)

    profile, country = profile_repo.get_profile_by_id(profile_id=profile_id)

    return GetProfileResponse(
                id=profile.id,
                name=profile.name,
                occupation=profile.occupation,
                personal_description=profile.personal_description,
                region=profile.region,
                country_name=country
            )


def update_profile_handler(
        request: CreateProfileRequest,
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        profile_repo: ProfileRepository = Depends()
):

    user: User = basic_authentication(token=token, user_repo=user_repo)

    if not request.profile_id:
        raise HTTPException(status_code=404, detail='profile id missed')

    profile, country = profile_repo.get_profile_by_id(profile_id=request.profile_id)

    profile.name = request.name
    profile.occupation = request.occupation
    profile.personal_description = request.personal_description
    profile.region = request.region
    profile.country_id = request.country_id

    profile: Profile = profile_repo.create_profile(profile)

    return CreateProfileResponse(message="Profile updated", data=profile)


def delete_profile_handler(
        profile_id: int,
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        profile_repo: ProfileRepository = Depends()
):

    user: User = basic_authentication(token=token, user_repo=user_repo)

    profile: Profile = profile_repo.delete_profile(profile_id=profile_id)

    return CreateProfileResponse(message="Profile deleted", data=profile)



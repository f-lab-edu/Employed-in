from fastapi import HTTPException, Header, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.profile import Profile, Country, Skill, UserSkill
from src.models.accounts import User
from src.service.accounts import UserService
from src.models.repository import ProfileRepository, UserRepository, SkillRepository
from src.schema.request import CreateProfileRequest, RegisterSkillRequest

from src.schema.response import CreateProfileResponse, GetProfileResponse, GetCountryResponse, RegisterSkillResponse, SkillResponse
from src.interfaces.permission import get_access_token, Auths


def profile_create_handler(
    request: CreateProfileRequest,
    token: str = Depends(get_access_token),
    user_repo: UserRepository = Depends(),
    profile_repo: ProfileRepository = Depends()
    ):

    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

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
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

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
        key=lambda profile: profile.id,
    )


def profile_handler(
        profile_id: int,
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        profile_repo: ProfileRepository = Depends(),
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    profile, country = profile_repo.get_profile_by_id(profile_id=profile_id, user_id=user.id)

    if not profile:
        raise HTTPException(status_code=400, detail="Invalid profile id")

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

    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    if not request.profile_id:
        raise HTTPException(status_code=400, detail='profile id missed')

    profile, country = profile_repo.get_profile_by_id(profile_id=request.profile_id, user_id=user.id)

    if not profile:
        raise HTTPException(status_code=400, detail='Invalid profile id')

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

    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    profile: Profile | None = profile_repo.delete_profile(profile_id=profile_id, user_id=user.id)

    return CreateProfileResponse(message="Profile deleted", data=profile)


def get_country_list_handler(
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        profile_repo: ProfileRepository = Depends()
):
    Auths.basic_authentication(token=token, user_repo=user_repo)

    countries: list[Country] = profile_repo.get_country_list()

    return sorted(
        [
            GetCountryResponse(
                id=country[0].id,
                name=country[0].name
            )
            for country in countries
        ],
        key=lambda country: country.id
    )


def register_skill_handler(
        request: RegisterSkillRequest,
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        skill_repo: SkillRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    if request.id is not None:
        if not skill_repo.skill_validation(skill_id=request.id, skill_name=request.name):
            raise HTTPException(status_code=400, detail="Skill id and name is not match")

        relation = UserSkill(user_id=user.id, skill_id=request.id)

    else:
        skill = Skill(name=request.name)

        new_skill: Skill = skill_repo.register_new_skill(skill)

        relation = UserSkill(user_id=user.id, skill_id=new_skill.id)

    new_relation: UserSkill = skill_repo.register_user_skill(user_skill=relation)

    return RegisterSkillResponse(message="Skill is registered")


def get_skill_list_handler(
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        skill_repo: SkillRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    skill_list: list[Skill] = skill_repo.get_all_skill_list()

    return sorted(
        [
            SkillResponse(
                id=skill[0].id,
                name=skill[0].name
            )
            for skill in skill_list
        ],
        key=lambda skill: skill.id
    )


def filter_registered_skill_handler(
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        skill_repo: SkillRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    skill_list: list[(UserSkill, Skill)] = skill_repo.filter_user_skill(user_id=user.id)

    return sorted(
        [
            SkillResponse(
                id=skill.id,
                name=skill.name
            )
            for relation, skill in skill_list
        ],
        key=lambda skill: skill.id
    )


def delete_registered_skill_handler(
        skill_id: int,
        token: str = Depends(get_access_token),
        user_repo: UserRepository = Depends(),
        skill_repo: SkillRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    relation: UserSkill = skill_repo.delete_registered_skill(user_id=user.id, skill_id=skill_id)

    return RegisterSkillResponse(message="Skill is deleted")

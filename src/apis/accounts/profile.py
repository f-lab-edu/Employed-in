from fastapi import HTTPException, Depends

from src.models.profile import Profile, Country, Skill, Career, Enterprise, Education
from src.models.accounts import User
from src.models.repository import AccountRepository
from src.schema.request import CreateProfileRequest, RegisterSkillRequest, RegisterCareerRequest, CreateEnterpriseRequest, RegisterEducationRequest

from src.schema.response import CreateProfileResponse, GetProfileResponse, GetCountryResponse, RegisterSkillResponse, SkillResponse, GetCareerResponse, GetEducationResponse, GetEnterpriseResponse, GetEnterprisesResponse
from src.interfaces.permission import get_access_token, Auths


async def profile_create_handler(
    request: CreateProfileRequest,
    token: str = Depends(get_access_token),
    account_repo: AccountRepository = Depends()
):

    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Profile")

    new_profile: Profile = Profile(
        name=request.name,
        occupation=request.occupation,
        personal_description=request.personal_description,
        region=request.region,
        country_id=request.country_id,
        user_id=user.id
    )
    user.profiles.append(new_profile)

    await account_repo.add_object(user)

    return CreateProfileResponse(message="New profile created", data=new_profile)


async def profile_lists_handler(
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Profile")

    return sorted(
        [
            GetProfileResponse(
                id=profile.id,
                name=profile.name,
                occupation=profile.occupation,
                personal_description=profile.personal_description,
                region=profile.region,
                country_name=profile.country.name
            )
            for profile in user.profiles
        ],
        key=lambda profile: profile.id,
    )


async def profile_handler(
        profile_id: int,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends(),
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    profile = await account_repo.get_obj_by_id(obj=Profile, obj_id=profile_id)

    if not profile or profile.user_id != user.id:
        raise HTTPException(status_code=400, detail="Invalid profile id")

    return GetProfileResponse(
                id=profile.id,
                name=profile.name,
                occupation=profile.occupation,
                personal_description=profile.personal_description,
                region=profile.region,
                country_name=profile.country.name
            )


async def update_profile_handler(
        request: CreateProfileRequest,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):

    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    if not request.profile_id:
        raise HTTPException(status_code=400, detail='profile id missed')

    profile = await account_repo.get_obj_by_id(obj=Profile, obj_id=request.profile_id)

    if not profile or profile.user_id != user.id:
        raise HTTPException(status_code=400, detail='Invalid profile id')

    profile.name = request.name
    profile.occupation = request.occupation
    profile.personal_description = request.personal_description
    profile.region = request.region
    profile.country_id = request.country_id

    await account_repo.add_object(profile)

    return CreateProfileResponse(message="Profile updated", data=profile)


async def delete_profile_handler(
        profile_id: int,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):

    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    profile = await account_repo.get_obj_by_id(obj=Profile, obj_id=profile_id)

    if not profile or profile.user_id != user.id:
        raise HTTPException(status_code=400, detail='Invalid profile id')

    profile: Profile | None = await account_repo.delete_object(obj=profile)

    return CreateProfileResponse(message="Profile deleted", data=profile)


async def get_country_list_handler(
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    await Auths.basic_authentication(token=token, account_repo=account_repo)

    countries: list[Country] = await account_repo.get_all_obj(obj=Country)

    return sorted(
        [
            GetCountryResponse(
                id=country.id,
                name=country.name
            )
            for country in countries
        ],
        key=lambda country: country.id
    )


async def register_skill_handler(
        request: RegisterSkillRequest,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends(),
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Skill")

    if request.id is not None:
        skill = await account_repo.get_obj_by_id(obj=Skill, obj_id=request.id)

    else:
        skill_obj = Skill(name=request.name)

        skill: Skill = await account_repo.add_object(skill_obj)

    user.skills.append(skill)

    await account_repo.add_object(obj=user)

    return RegisterSkillResponse(message="Skill is registered")


async def get_skill_list_handler(
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    skill_list = await account_repo.get_all_obj(obj=Skill)

    return sorted(
        [
            SkillResponse(
                id=skill.id,
                name=skill.name
            )
            for skill in skill_list
        ],
        key=lambda skill: skill.id
    )


async def filter_registered_skill_handler(
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Skill")

    return sorted(
        [
            SkillResponse(
                id=skill.id,
                name=skill.name
            )
            for skill in user.skills
        ],
        key=lambda skill: skill.id
    )


async def delete_registered_skill_handler(
        skill_id: int,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Skill")

    skills = [skill for skill in user.skills if skill.id != skill_id]

    user.skills = skills

    await account_repo.add_object(user)

    return RegisterSkillResponse(message="Skill is deleted")


async def register_career_handler(
        request: RegisterCareerRequest,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    career = Career(
        position=request.position,
        description=request.description,
        start_time=request.start_time,
        end_time=request.end_time,
        enterprise_id=request.enterprise_id,
        employment_type_id=request.employment_type_id
    )

    new_career: Career = await account_repo.add_object(career)

    user.careers.append(new_career)

    await account_repo.add_object(user)

    return RegisterSkillResponse(message="Career is registered")


async def get_career_list_handler(
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Career")

    return sorted(
        [
            GetCareerResponse(
                id=career.id,
                position=career.position,
                description=career.description,
                start_time=career.start_time,
                end_time=career.end_time,
                employment_type_id=career.employment_type.id,
                employment_type_name=career.employment_type.name,
                enterprise_id=career.enterprise.id,
                enterprise_name=career.enterprise.name
            )
            for career in user.careers
        ],
        key=lambda career: career.id
    )


async def update_career_handler(
        request: RegisterCareerRequest,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Career")

    career: Career = await account_repo.get_obj_by_id(Career, request.id)

    if career.id not in [reg_career.id for reg_career in user.careers]:
        raise HTTPException(status_code=400, detail="Invalid Career id")

    career.position = request.position
    career.description = request.description
    career.start_time = request.start_time
    career.end_time = request.end_time
    career.enterprise_id = request.enterprise_id
    career.employment_type_id = request.employment_type_id

    career: Career = await account_repo.add_object(career)

    return RegisterSkillResponse(message="career updated")


async def delete_career_handler(
        career_id: int,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Career")

    career: Career = await account_repo.get_obj_by_id(Career, career_id)

    if career.id not in [reg_career.id for reg_career in user.careers]:
        raise HTTPException(status_code=400, detail="Invalid Career id")

    deleted_career: Career = await account_repo.delete_object(career)

    return RegisterSkillResponse(message="Career is deleted")


async def register_new_enterprise_handler(
        request: CreateEnterpriseRequest,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    enterprise = Enterprise(
        name=request.name,
        description=request.description,
        enterprise_type_id=request.enterprise_type_id,
        industry_id=request.industry_id,
        country_id=request.country_id
    )

    new_enterprise: Enterprise = await account_repo.add_object(enterprise)

    return RegisterSkillResponse(message="enterprise registered")


async def enterprises_handler(
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    enterprises: list[Enterprise] = await account_repo.get_all_obj(Enterprise)

    return sorted(
        [
            GetEnterprisesResponse(
                id=enterprise.id,
                name=enterprise.name,
                description=enterprise.description
            )
            for enterprise in enterprises
        ],
        key=lambda enterprise: enterprise.id
    )


async def enterprise_handler(
        enterprise_id: int,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo)

    enterprise: Enterprise = await account_repo.get_obj_by_id(Enterprise, enterprise_id)

    return GetEnterpriseResponse(
        id=enterprise.id,
        name=enterprise.name,
        description=enterprise.description,
        enterprise_type_name=enterprise.enterprise_type.name,
        industry_name=enterprise.industry.name,
        country_name=enterprise.country.name
    )


async def register_education_handler(
        request: RegisterEducationRequest,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Education")

    education = Education(
        major=request.major,
        start_time=request.start_time,
        graduate_time=request.graduate_time,
        grade=request.grade,
        degree_type=request.degree_type,
        description=request.description,
        enterprise_id=request.enterprise_id
    )

    new_education: Education = await account_repo.add_object(education)

    user.educations.append(new_education)

    await account_repo.add_object(user)

    return RegisterSkillResponse(message="Education is registered")


async def get_education_list_handler(
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Education")

    return sorted(
        [
            GetEducationResponse(
                id=education.id,
                major=education.major,
                description=education.description,
                start_time=education.start_time,
                graduate_time=education.graduate_time,
                grade=education.grade,
                degree_type=education.degree_type,
                enterprise_id=education.enterprise.id,
                enterprise_name=education.enterprise.name
            )
            for education in user.educations
        ],
        key=lambda education: education.id
    )


async def update_education_handler(
        request: RegisterEducationRequest,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Education")

    education: Education = await account_repo.get_obj_by_id(Education, request.id)

    if education.id not in [reg_edu.id for reg_edu in user.educations]:
        raise HTTPException(status_code=400, detail="Invalid education id")

    education.major = request.major
    education.start_time = request.start_time
    education.graduate_time = request.graduate_time
    education.grade = request.grade
    education.degree_type = request.degree_type
    education.description = request.description

    education: Education = await account_repo.add_object(education)

    return RegisterSkillResponse(message="education updated")


async def delete_education_handler(
        education_id: int,
        token: str = Depends(get_access_token),
        account_repo: AccountRepository = Depends()
):
    user: User = await Auths.basic_authentication(token=token, account_repo=account_repo, relation="Education")

    education: Education = await account_repo.get_obj_by_id(Education, education_id)

    if education.id not in [reg_edu.id for reg_edu in user.educations]:
        raise HTTPException(status_code=400, detail="Invalid education id")

    deleted_career: Education = await account_repo.delete_object(education)

    return RegisterSkillResponse(message="Education is deleted")

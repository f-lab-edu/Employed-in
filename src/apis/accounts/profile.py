from fastapi import HTTPException, Header, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.profile import Profile, Country, Skill, UserSkill, Career, UserCareer, Enterprise, Education, UserEducation, Industry, EnterpriseType, EmploymentType
from src.models.accounts import User
from src.service.accounts import UserService
from src.models.repository import AccountRepository
from src.schema.request import CreateProfileRequest, RegisterSkillRequest, RegisterCareerRequest, CreateEnterpriseRequest, RegisterEducationRequest

from src.schema.response import CreateProfileResponse, GetProfileResponse, GetCountryResponse, RegisterSkillResponse, SkillResponse, GetCareerResponse, GetEducationResponse, GetEnterpriseResponse, GetEnterprisesResponse
from src.interfaces.permission import get_access_token, Auths


def profile_create_handler(
    request: CreateProfileRequest,
    token: str = Depends(get_access_token),
    user_repo: AccountRepository = Depends()
):

    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Profile")

    new_profile: Profile = Profile(
        name=request.name,
        occupation=request.occupation,
        personal_description=request.personal_description,
        region=request.region,
        country_id=request.country_id,
        user_id=user.id
    )
    user.profiles.append(new_profile)

    user_repo.add_object(user)

    return CreateProfileResponse(message="New profile created", data=new_profile)


def profile_lists_handler(
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Profile")

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
            for profile, country in user.profiles
        ],
        key=lambda profile: profile.id,
    )


def profile_handler(
        profile_id: int,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends(),
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    profile = user_repo.get_obj_by_id(obj=Profile, obj_id=profile_id)

    if not profile:
        raise HTTPException(status_code=400, detail="Invalid profile id")

    return GetProfileResponse(
                id=profile.id,
                name=profile.name,
                occupation=profile.occupation,
                personal_description=profile.personal_description,
                region=profile.region,
                country_name=profile.country.name
            )


def update_profile_handler(
        request: CreateProfileRequest,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):

    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Profile")

    if not request.profile_id:
        raise HTTPException(status_code=400, detail='profile id missed')

    profile = user_repo.get_obj_by_id(obj=Profile, obj_id=request.profile_id)

    if not profile or profile.user_id != user.id:
        raise HTTPException(status_code=400, detail='Invalid profile id')

    profile.name = request.name
    profile.occupation = request.occupation
    profile.personal_description = request.personal_description
    profile.region = request.region
    profile.country_id = request.country_id

    user_repo.add_object(user)

    return CreateProfileResponse(message="Profile updated", data=profile)


def delete_profile_handler(
        profile_id: int,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):

    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    profile = user_repo.get_obj_by_id(obj=Profile, obj_id=profile_id)

    if not profile or profile.user_id != user.id:
        raise HTTPException(status_code=400, detail='Invalid profile id')

    profile: Profile | None = user_repo.delete_object(obj=profile)

    return CreateProfileResponse(message="Profile deleted", data=profile)


def get_country_list_handler(
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    Auths.basic_authentication(token=token, user_repo=user_repo)

    countries: list[Country] = user_repo.get_all_obj(obj=Country)

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
        user_repo: AccountRepository = Depends(),
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Skill")

    if request.id is not None:
        skill = user_repo.get_obj_by_id(obj=Skill, obj_id=request.id)

    else:
        skill_obj = Skill(name=request.name)

        skill: Skill = user_repo.add_object(skill_obj)

    user.skills.append(skill)

    user_repo.add_object(obj=user)

    return RegisterSkillResponse(message="Skill is registered")


def get_skill_list_handler(
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    skill_list = user_repo.get_all_obj(obj=Skill)

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
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Skill")

    return sorted(
        [
            SkillResponse(
                id=skill.id,
                name=skill.name
            )
            for relation, skill in user.skills
        ],
        key=lambda skill: skill.id
    )


def delete_registered_skill_handler(
        skill_id: int,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Skill")

    skills = [skill for skill in user.skills if skill.id != skill_id]

    user.skills = skills

    user_repo.add_object(user)

    return RegisterSkillResponse(message="Skill is deleted")


def register_career_handler(
        request: RegisterCareerRequest,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    career = Career(
        position=request.position,
        description=request.description,
        start_time=request.start_time,
        end_time=request.end_time,
        enterprise_id=request.enterprise_id,
        employment_type_id=request.employment_type_id
    )

    new_career: Career = user_repo.add_object(career)

    user.careers.append(new_career)

    user_repo.add_object(user)

    return RegisterSkillResponse(message="Career is registered")


def get_career_list_handler(
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Career")

    emp_types = user_repo.get_all_obj(EmploymentType)

    employment_type = {
        emp_type[0].id : emp_type[0].name for emp_type in emp_types
    }

    return sorted(
        [
            GetCareerResponse(
                id=career.id,
                position=career.position,
                description=career.description,
                start_time=career.start_time,
                end_time=career.end_time,
                employment_type_id=career.employment_type_id,
                employment_type_name=employment_type[career.employment_type_id],
                enterprise_id=career.enterprise_id
            )
            for relation, career in user.careers
        ],
        key=lambda career: career.id
    )


def update_career_handler(
        request: RegisterCareerRequest,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Career")

    career: Career = user_repo.get_obj_by_id(Career, request.id)

    career.position = request.position
    career.description = request.description
    career.start_time = request.start_time
    career.end_time = request.end_time
    career.enterprise_id = request.enterprise_id
    career.employment_type_id = request.employment_type_id

    career: Career = user_repo.add_object(career)

    return RegisterSkillResponse(message="career updated")


def delete_career_handler(
        career_id: int,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    career: Career = user_repo.get_obj_by_id(Career, career_id)

    deleted_career: Career = user_repo.delete_object(career)

    return RegisterSkillResponse(message="Career is deleted")


def register_new_enterprise_handler(
        request: CreateEnterpriseRequest,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    enterprise = Enterprise(
        name=request.name,
        description=request.description,
        enterprise_type_id=request.enterprise_type_id,
        industry_id=request.industry_id,
        country_id=request.country_id
    )

    new_enterprise: Enterprise = user_repo.add_object(enterprise)

    return RegisterSkillResponse(message="enterprise registered")


def enterprises_handler(
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    enterprises: list[Enterprise] = career_repo.get_all_obj(Enterprise)

    return sorted(
        [
            GetEnterprisesResponse(
                id=enterprise[0].id,
                name=enterprise[0].name,
                description=enterprise[0].description
            )
            for enterprise in enterprises
        ],
        key=lambda enterprise: enterprise.id
    )


def enterprise_handler(
        enterprise_id: int,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    enterprise: Enterprise = user_repo.get_obj_by_id(Enterprise, enterprise_id)

    industry: Industry = user_repo.get_obj_by_id(Industry, enterprise.industry_id)

    country: Country = user_repo.get_obj_by_id(Country, enterprise.country_id)

    enterprise_type: EnterpriseType = user_repo.get_obj_by_id(EnterpriseType, enterprise.enterprise_type_id)

    return GetEnterpriseResponse(
        id=enterprise.id,
        name=enterprise.name,
        description=enterprise.description,
        enterprise_type_name=enterprise_type.name,
        industry_name=industry.name,
        country_name=country.name
    )


def register_education_handler(
        request: RegisterEducationRequest,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Education")

    education = Education(
        major=request.major,
        start_time=request.start_time,
        graduate_time=request.graduate_time,
        grade=request.grade,
        degree_type=request.degree_type,
        description=request.description,
        enterprise_id=request.enterprise_id
    )

    new_education: Education = user_repo.add_object(education)

    user.educations.append(new_education)

    user_repo.add_object(user)

    return RegisterSkillResponse(message="Education is registered")


def get_education_list_handler(
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Education")

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
                enterprise_id=education.enterprise_id,
                enterprise_name=education.enterprise_name
            )
            for education in user.educations
        ],
        key=lambda education: education.id
    )


def update_education_handler(
        request: RegisterEducationRequest,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo)

    education: Education = user_repo.get_obj_by_id(Education, request.id)

    education.major = request.major
    education.start_time = request.start_time
    education.graduate_time = request.graduate_time
    education.grade = request.grade
    education.degree_type = request.degree_type
    education.description = request.description

    education: Education = user_repo.add_object(education)

    return RegisterSkillResponse(message="education updated")


def delete_education_handler(
        education_id: int,
        token: str = Depends(get_access_token),
        user_repo: AccountRepository = Depends()
):
    user: User = Auths.basic_authentication(token=token, user_repo=user_repo, relation="Education")

    education: Education = user_repo.get_obj_by_id(Education, education_id)

    deleted_career: Education = user_repo.delete_object(education)

    return RegisterSkillResponse(message="Education is deleted")

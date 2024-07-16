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
account_router.add_api_route(
    methods=["GET"],
    path="/countries",
    endpoint=profile.get_country_list_handler,
    response_model=list[response.GetCountryResponse],
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["POST"],
    path="/skills",
    endpoint=profile.register_skill_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["GET"],
    path="/skills/registered",
    endpoint=profile.filter_registered_skill_handler,
    response_model=list[response.SkillResponse],
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["GET"],
    path="/skills",
    endpoint=profile.get_skill_list_handler,
    response_model=list[response.SkillResponse],
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["DELETE"],
    path="/skills/registered/{skill_id}",
    endpoint=profile.delete_registered_skill_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["POST"],
    path="/careers",
    endpoint=profile.register_career_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["GET"],
    path="/careers",
    endpoint=profile.get_career_list_handler,
    response_model=list[response.GetCareerResponse],
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["PATCH"],
    path="/careers",
    endpoint=profile.update_career_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["DELETE"],
    path="/careers/{career_id}",
    endpoint=profile.delete_career_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["POST"],
    path="/enterprises",
    endpoint=profile.register_new_enterprise_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["GET"],
    path="/enterprises",
    endpoint=profile.enterprises_handler,
    response_model=list[response.GetEnterprisesResponse],
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["GET"],
    path="/enterprises/{enterprise_id}",
    endpoint=profile.enterprise_handler,
    response_model=response.GetEnterpriseResponse,
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["POST"],
    path="/educations",
    endpoint=profile.register_education_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["GET"],
    path="/educations",
    endpoint=profile.get_education_list_handler,
    response_model=list[response.GetEducationResponse],
    status_code=status.HTTP_200_OK
)
account_router.add_api_route(
    methods=["PATCH"],
    path="/educations",
    endpoint=profile.update_education_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_201_CREATED
)
account_router.add_api_route(
    methods=["DELETE"],
    path="/educations/{education_id}",
    endpoint=profile.delete_education_handler,
    response_model=response.RegisterSkillResponse,
    status_code=status.HTTP_200_OK
)

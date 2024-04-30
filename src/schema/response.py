from pydantic import BaseModel

from src.models.profile import Profile, Skill


class JWTResponse(BaseModel):
    access_token: str


class CreateProfileResponse(BaseModel):
    message: str
    data: Profile


class GetProfileResponse(BaseModel):
    id: int
    name: str
    occupation: str
    personal_description: str
    region: str
    country_name: str


class GetCountryResponse(BaseModel):
    id: int
    name: str


class RegisterSkillResponse(BaseModel):
    message: str


class SkillResponse(BaseModel):
    id: int
    name: str

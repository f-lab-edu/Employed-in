from pydantic import BaseModel
from typing import Optional
from datetime import date

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


class GetCareerResponse(BaseModel):
    id: int
    position: str
    description: str
    start_time: date
    end_time: date | None
    employment_type_id: int
    employment_type_name: str
    enterprise_id: int
    enterprise_name: str


class GetEducationResponse(BaseModel):
    id: int
    major: str
    description: str
    start_time: date
    graduate_time: date | None
    grade: str
    degree_type: str
    enterprise_id: int
    enterprise_name: str


class GetEnterpriseResponse(BaseModel):
    id: int
    name: str
    description: str
    enterprise_type_name: str
    industry_name: str
    country_name: str


class GetEnterprisesResponse(BaseModel):
    id: int
    name: str
    description: str
from pydantic import BaseModel

from src.models.profile import Profile


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

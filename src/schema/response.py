from pydantic import BaseModel

from src.models.profile import Profile

class JWTResponse(BaseModel):
    access_token: str


class CreateProfileResponse(BaseModel):
    message: str
    data: Profile

from pydantic import BaseModel


class JWTResponse(BaseModel):
    access_token: str

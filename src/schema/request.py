from fastapi import HTTPException
from typing import Optional
from pydantic import BaseModel, field_validator


class SignUpRequest(BaseModel):
    email: str
    phone_number: str
    password: str
    confirm_password: str
    nickname: Optional[str] = None
    is_business: bool
    membership_id: Optional[int] = 1

    @field_validator("password")
    def validate_password(self, password):
        if self.confirm_password != password:
            raise HTTPException(status_code=400, detail="Input password is not match with confirmed password")

        errors = {}

        if len(password) < 8:
            errors["length"] = "Password length should be longer than 8"

        return password


class LoginRequest(BaseModel):
    email: str
    password: str

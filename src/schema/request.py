import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator


class SignUpRequest(BaseModel):
    email: EmailStr
    phone_number: str
    confirm_password: str
    password: str
    nickname: Optional[str] = None
    is_business: Optional[bool] = False
    membership_id: Optional[int] = 1

    @field_validator("password")
    @classmethod
    def validate_password(cls, password, values):
        if values.data["confirm_password"] != password:
            raise HTTPException(
                status_code=400,
                detail="Input password is not match with confirmed password",
            )

        upper = re.compile("^(?=.*?[A-Z])")
        lower = re.compile("^(?=.*?[a-z])")
        digit = re.compile("^(?=.*?[0-9])")
        special = re.compile("^(?=.*?[#?!@$%^&*-])")

        errors = {}

        if len(password) < 8:
            errors["length"] = "Password length should be longer than 8"
        if not re.match(upper, password):
            errors["upper"] = "Password should include at least one uppercase letter"
        if not re.match(lower, password):
            errors["lower"] = "Password should include at least one lowercase letter"
        if not re.match(digit, password):
            errors["digit"] = "Password should include at least one digit"
        if not re.match(special, password):
            errors["special"] = "Password should include at least one special character"

        if len(errors) > 0:
            raise HTTPException(status_code=400, detail=errors)

        return password


class LoginRequest(BaseModel):
    email: str
    password: str

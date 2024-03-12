from typing import Optional
from pydantic import BaseModel


class SignUpRequest(BaseModel):
    email: str
    phone_number: str
    password: str
    confirm_password: str
    nickname: Optional[str] = None
    is_business: bool
    membership_id: Optional[int] = 1

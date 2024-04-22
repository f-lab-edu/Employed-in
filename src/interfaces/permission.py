from fastapi import HTTPException, Header, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.models.accounts import User
from src.service.accounts import UserService
from src.models.repository import UserRepository


#def basic_authentication(token: str, user_service: UserService = Depends(), user_repo: UserRepository = Depends()) -> User:

def get_access_token(auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))) -> str:
    if auth_header is None:
        raise HTTPException(status_code=401, detail="No auth credential")

    return auth_header.credentials


def basic_authentication(token: str, user_repo: UserRepository) -> User:
    verified = UserService().decode_jwt(access_token=token)

    if not verified:
        raise HTTPException(status_code=403, detail="Invalid token")

    user = user_repo.get_user_by_email(user_email=verified)

    if not user:
        raise HTTPException(status_code=403, detail="No user")

    return user

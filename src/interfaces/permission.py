from fastapi import HTTPException, Header, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.models.accounts import User
from src.service.accounts import UserService
from src.models.repository import AccountRepository


#def basic_authentication(token: str, user_service: UserService = Depends(), account_repo: UserRepository = Depends()) -> User:

def get_access_token(auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))) -> str:
    if auth_header is None:
        raise HTTPException(status_code=401, detail="No auth credential")

    return auth_header.credentials


class Auths:
    @staticmethod
    def basic_authentication(token: str, account_repo: AccountRepository, relation=None) -> User:
        verified = UserService().decode_jwt(access_token=token)

        if not verified:
            raise HTTPException(status_code=403, detail="Invalid token")

        if relation:
            user = account_repo.get_user_with_relation(user_email=verified, relation=relation)
        else:
            user = account_repo.get_user_by_email(user_email=verified)

        if not user:
            raise HTTPException(status_code=403, detail="No user")

        return user

    def admin_permission(self, token: str, account_repo: AccountRepository) -> User:
        user: User = self.basic_authentication(token=token, account_repo=account_repo)

        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Only admin user allowed")

        return user


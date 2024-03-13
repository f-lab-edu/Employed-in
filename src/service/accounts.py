import os
import bcrypt

from datetime import datetime, timedelta
from jose import jwt


class UserService:
    encoding: str = os.getenv("ENCODING", "UTF-8")
    secret_key: str = os.getenv("SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS512")

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    def create_jwt(self, user_email: str) -> str:
        return jwt.encode(
        {
            "sub": user_email,
            "exp": datetime.now() + timedelta(days=7)
        },
            self.secret_key,
            algorithm=self.jwt_algorithm
        )

    def decode_jwt(self, access_token: str) -> int:
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        return payload["sub"]

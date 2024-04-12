from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.accounts import User


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_user_by_email(self, user_email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == user_email))

    def create_user(self, user: User) -> User:
        user.is_admin = False
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user

    def create_admin_user(self, user: User) -> User:
        user.is_admin = True
        return self.create_user(user)

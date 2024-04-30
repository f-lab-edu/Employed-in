from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.accounts import User
from src.models.profile import Profile, UserCareer, Career, Country


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_user_by_email(self, user_email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == user_email))

    def create_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user

    def create_admin_user(self, user: User) -> User:
        user.is_admin = True
        return self.create_user(user)


class ProfileRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def profile_validation(self, user_id: int, country_id: int) -> bool:
        exists = self.session.scalar(select(Profile).where(Profile.user_id ==user_id, Profile.country_id == country_id))

        return False if exists else True

    def filter_profile_by_user(self, user_id: int) -> list[(Profile, Country)]:
        return list(self.session.execute(select(Profile, Country.name).join(Country).where(Profile.user_id == user_id)))

    def get_profile_by_id(self, profile_id: int, user_id: int):
        result = self.session.execute(select(Profile, Country.name).join(Country).where(Profile.id == profile_id, Profile.user_id == user_id)).fetchone()

        if not result:
            return (None, None)

        return (result[0], result[1])

    def create_profile(self, profile: Profile) -> Profile:
        self.session.add(instance=profile)
        self.session.commit()
        self.session.refresh(instance=profile)
        return profile

    def delete_profile(self, profile_id: int, user_id: int) -> Profile | None:
        profile, country = self.get_profile_by_id(profile_id=profile_id, user_id=user_id)

        if not profile:
            return None

        self.session.delete(profile)
        self.session.commit()
        return profile

    def get_country_list(self) -> list[Country]:
        return list(self.session.execute(select(Country)))
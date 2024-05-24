from fastapi import Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload
from abc import abstractmethod, ABCMeta, ABC

from src.database import get_db
from src.models.accounts import User
from src.models.profile import Profile, UserCareer, Career, Country, Skill, UserSkill, UserEducation, Education


class BaseRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def add_object(self, obj):
        self.session.add(instance=obj)
        self.session.commit()
        self.session.refresh(instance=obj)

        return obj

    def delete_object(self, obj):
        self.session.delete(obj)
        self.session.commit()
        return obj

    def get_obj_by_id(self, obj, obj_id: int):
        return self.session.scalar(select(obj).where(obj.id == obj_id))

    def get_all_obj(self, obj):
        return list(self.session.execute(select(obj)).scalars())

    def raw_query(self, statement):
        return list(self.session.execute(text(statement)).mappings().fetchall())


class AccountRepository(BaseRepository):

    def get_user_by_email(self, user_email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == user_email))

    def get_user_with_relation(self, user_email: str, relation) -> User | None:
        if relation == "Skill":
            return self.session.execute(select(User).options(selectinload(User.skills)).where(User.email == user_email)).scalar()

        elif relation == "Career":
            return self.session.execute(select(User).options(selectinload(User.careers)).where(User.email == user_email)).scalar()

        elif relation == "Profile":
            return self.session.execute(select(User).options(selectinload(User.profiles)).where(User.email == user_email)).scalar()

        elif relation == "Education":
            return self.session.execute(select(User).options(selectinload(User.educations)).where(User.email == user_email)).scalar()
        else:
            raise ValueError("Invalid Relation option")

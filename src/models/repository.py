from fastapi import Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload
from abc import abstractmethod, ABCMeta, ABC

from src.database import get_db, get_async_db
from src.models.accounts import User
from src.models.profile import Profile, UserCareer, Career, Country, Skill, UserSkill, UserEducation, Education


class BaseRepository:
    def __init__(self, session: Session = Depends(get_async_db)):
        self.session = session

    async def add_object(self, obj):
        self.session.add(instance=obj)
        await self.session.commit()
        await self.session.refresh(instance=obj)

        return obj

    async def delete_object(self, obj):
        self.session.delete(obj)
        await self.session.commit()
        return obj

    async def get_obj_by_id(self, obj, obj_id: int):
        return await self.session.scalar(select(obj).where(obj.id == obj_id))

    async def get_all_obj(self, obj):
        #return await self.session.execute(select(obj)).scalars()
        return list(await self.session.scalars(select(obj)))

    async def raw_query(self, statement):
        return await self.session.execute(text(statement)).mappings().fetchall()


class AccountRepository(BaseRepository):

    async def get_user_by_email(self, user_email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == user_email))

    async def get_user_with_relation(self, user_email: str, relation) -> User | None:
        if relation == "Skill":
            return await self.session.scalar(select(User).options(selectinload(User.skills)).where(User.email == user_email))

        elif relation == "Career":
            return await self.session.scalar(select(User).options(selectinload(User.careers)).where(User.email == user_email))

        elif relation == "Profile":
            return await self.session.scalar(select(User).options(selectinload(User.profiles)).where(User.email == user_email))

        elif relation == "Education":
            return await self.session.scalar(select(User).options(selectinload(User.educations)).where(User.email == user_email))
        else:
            raise ValueError("Invalid Relation option")

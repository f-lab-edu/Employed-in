from fastapi import Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session
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
        return list(self.session.execute(select(obj)))

    def get_relation_obj(self, relation_obj, obj1, obj2, obj1_id, obj2_id):
        return self.session.execute(select(relation_obj).where(obj1.id == obj1_id, obj2.id == obj2_id)).fetchone()[0]

    def raw_query(self, statement):
        return list(self.session.execute(text(statement)).mappings().fetchall())


class UserRepository(BaseRepository):

    def get_user_by_email(self, user_email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == user_email))


class ProfileRepository(BaseRepository):

    def profile_validation(self, user_id: int, country_id: int) -> bool:
        exists = self.session.scalar(select(Profile).where(Profile.user_id ==user_id, Profile.country_id == country_id))

        return False if exists else True

    def filter_obj(self, user_id: int) -> list[(Profile, Country)]:
        return list(self.session.execute(select(Profile, Country.name).join(Country).where(Profile.user_id == user_id)))

    def get_obj_by_id(self, profile_id: int, user_id: int):
        result = self.session.execute(select(Profile, Country.name).join(Country).where(Profile.id == profile_id, Profile.user_id == user_id)).fetchone()

        if not result:
            raise HTTPException(status_code=400, detail='Invalid profile id')

        return (result[0], result[1])

    def get_country_list(self) -> list[Country]:
        return list(self.session.execute(select(Country)))


class SkillRepository(BaseRepository):

    def skill_validation(self, skill_id: int, skill_name: str) -> bool:
        result: Skill = self.session.execute(select(Skill).where(Skill.id == skill_id)).fetchone()[0]

        return bool(result.name == skill_name)

    def filter_user_skill(self, user_id: int) -> list[(UserSkill, Skill)]:
        return list(self.session.execute(select(UserSkill, Skill).join(Skill).where(UserSkill.user_id == user_id)))


class CareerRepository(BaseRepository):

    def filter_user_career(self, user_id: int) -> list:
        statement = "select career.id, usercareer.id as relation_id, career.position, career.description, career.start_time, career.end_time, career.employment_type_id, career.enterprise_id from usercareer inner join career on career.id=usercareer.career_id where usercareer.user_id=:user_id;"

        return list(self.session.execute(text(statement), {"user_id": user_id}).mappings().fetchall())


class EducationRepository(BaseRepository):

    def filter_user_education(self, user_id: int) -> list:
        statement = "select usereducation.id as id, education.major, education.start_time, education.graduate_time, education.degree_type, education.grade, education.description, education.enterprise_id as enterprise_id, enterprise.name as enterprise_name from usereducation inner join education on education.id=usereducation.education_id inner join enterprise on enterprise.id=education.enterprise_id where usereducation.user_id=:user_id;"

        return list(self.session.execute(text(statement), {"user_id": user_id}).mappings().fetchall())

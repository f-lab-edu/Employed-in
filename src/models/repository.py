from fastapi import Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.accounts import User
from src.models.profile import Profile, UserCareer, Career, Country, Skill, UserSkill, Enterprise, EmploymentType


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
            raise HTTPException(status_code=400, detail='Invalid profile id')

        return (result[0], result[1])

    def create_profile(self, profile: Profile) -> Profile:
        self.session.add(instance=profile)
        self.session.commit()
        self.session.refresh(instance=profile)
        return profile

    def delete_profile(self, profile_id: int, user_id: int) -> Profile | None:
        profile, country = self.get_profile_by_id(profile_id=profile_id, user_id=user_id)

        self.session.delete(profile)
        self.session.commit()
        return profile

    def get_country_list(self) -> list[Country]:
        return list(self.session.execute(select(Country)))


class SkillRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def register_new_skill(self, skill: Skill) -> Skill:
        self.session.add(instance=skill)
        self.session.commit()
        self.session.refresh(instance=skill)
        return skill

    def register_user_skill(self, user_skill: UserSkill) -> UserSkill:
        self.session.add(instance=user_skill)
        self.session.commit()
        self.session.refresh(instance=user_skill)
        return user_skill

    def get_all_skill_list(self) -> list[Skill]:
        return list(self.session.execute(select(Skill)))

    def skill_validation(self, skill_id: int, skill_name: str) -> bool:
        result: Skill = self.session.execute(select(Skill).where(Skill.id == skill_id)).fetchone()[0]

        return bool(result.name == skill_name)

    def get_registered_relation(self, user_id: int, skill_id: int) -> UserSkill:
        return self.session.execute(select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id)).fetchone()[0]

    def filter_user_skill(self, user_id: int) -> list[(UserSkill, Skill)]:
        return list(self.session.execute(select(UserSkill, Skill).join(Skill).where(UserSkill.user_id == user_id)))

    def delete_registered_skill(self, user_id: int, skill_id: int) -> UserSkill:
        relation: UserSkill = self.get_registered_relation(user_id=user_id, skill_id=skill_id)

        if not relation:
            raise HTTPException(status_code=400, detail="Skill id is not registered")

        self.session.delete(relation)
        self.session.commit()
        return relation


class CareerRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def register_new_career(self, career: Career) -> Career:
        self.session.add(instance=career)
        self.session.commit()
        self.session.refresh(instance=career)
        return career

    def register_user_skill(self, user_career: UserCareer) -> UserCareer:
        self.session.add(instance=user_career)
        self.session.commit()
        self.session.refresh(instance=user_career)
        return user_career

    def get_career_by_id(self, career_id: int) -> Career:
        result: Career = self.session.execute(select(Career).where(Career.id == career_id))

        if not result:
            raise HTTPException(status_code=400, detail='Invalid career id')

        return result

    def get_registered_relation(self, user_id: int, career_id: int) -> UserCareer:
        return self.session.execute(
            select(UserCareer).where(UserCareer.user_id == user_id, UserCareer.career_id == career_id)).fetchone()[0]

    def filter_user_career(self, user_id: int) -> list:
        statement = "select usercareer.id, career.position, career.description, career.start_time, career.end_time, career.employment_type_id, enterprise.name from usercareer inner join career on career.id=usercareer.career_id inner join enterprise on enterprise.id=career.enterprise_id where usercareer.user_id=:user_id;"

        return list(self.session.execute(text(statement), {"user_id": user_id}).mappings().fetchall())

    def delete_career(self, user_id: int, career_id: int) -> UserCareer:
        relation: UserCareer = self.get_registered_relation(user_id=user_id, career_id=career_id)

        if not relation:
            raise HTTPException(status_code=400, detail="Skill id is not registered")

        career: Career = self.get_career_by_id(career_id=career_id)

        self.session.delete(career)
        self.session.delete(relation)
        self.session.commit()

        return relation

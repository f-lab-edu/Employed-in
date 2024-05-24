import datetime

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint
from typing import Optional


class UserEducation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    education_id: int = Field(foreign_key="education.id")


class UserEnterprise(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    enterprise_id: int = Field(foreign_key="enterprise.id")


class UserCareer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    career_id: int = Field(foreign_key="career.id")


class UserSkill(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("skill_id", "user_id", name="userskill_uq"),
    )
    user_id: int | None = Field(foreign_key="user.id", default=None, primary_key=True)
    skill_id: int | None = Field(foreign_key="skill.id", default=None, primary_key=True)


class EnterpriseType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)

    enterprises: list["Enterprise"] = Relationship(back_populates="enterprise_type")


class Industry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)

    enterprises: list["Enterprise"] = Relationship(back_populates="industry")


class Country(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)

    profiles: list["Profile"] = Relationship(back_populates="country")
    enterprises: list["Enterprise"] = Relationship(back_populates="country")


class Skill(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=30)

    users: list["User"] = Relationship(back_populates="skills", link_model=UserSkill)


class EmploymentType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=20)

    careers: list["Career"] = Relationship(back_populates="employment_type")


class Profile(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("country_id", "user_id", name="profile_uq"),
    )
    id: int = Field(primary_key=True)
    name: str = Field(nullable=True, max_length=30)
    occupation: str = Field(nullable=True, max_length=30)
    personal_description: str = Field(nullable=True, max_length=255)
    region: str = Field(nullable=True, max_length=50)
    country_id: int = Field(foreign_key="country.id")
    user_id: int = Field(foreign_key="user.id")

    country: Country | None = Relationship(back_populates="profiles", sa_relationship_kwargs=dict(lazy="joined"))
    user: "User" = Relationship(back_populates="profiles")


class Education(SQLModel, table=True):
    id: int = Field(primary_key=True)
    major: str = Field(max_length=50)
    start_time: datetime.datetime = Field()
    graduate_time: datetime.datetime = Field(nullable=True, default=None)
    grade: str = Field(nullable=True, max_length=10)
    degree_type: str = Field(max_length=20)
    description: str = Field(nullable=True, max_length=45)
    enterprise_id: int = Field(foreign_key="enterprise.id")

    users: list["User"] = Relationship(back_populates="educations", link_model=UserEducation)
    enterprise: "Enterprise" = Relationship(back_populates="educations", sa_relationship_kwargs=dict(lazy="joined"))


class Enterprise(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(max_length=255)
    enterprise_type_id: int = Field(foreign_key="enterprisetype.id")
    industry_id: int = Field(foreign_key="industry.id")
    country_id: int = Field(foreign_key="country.id")

    country: Country | None = Relationship(back_populates="enterprises", sa_relationship_kwargs=dict(lazy="joined"))
    industry: Industry | None = Relationship(back_populates="enterprises", sa_relationship_kwargs=dict(lazy="joined"))
    enterprise_type: EnterpriseType | None = Relationship(back_populates="enterprises", sa_relationship_kwargs=dict(lazy="joined"))
    careers: list["Career"] = Relationship(back_populates="enterprise")
    educations: list[Education] = Relationship(back_populates="enterprise")


class Career(SQLModel, table=True):
    id: int = Field(primary_key=True)
    position: str = Field(max_length=30)
    description: str = Field(nullable=True, default=None, max_length=255)
    start_time: datetime.datetime = Field()
    end_time: datetime.datetime = Field(nullable=True, default=None)
    enterprise_id: int = Field(foreign_key="enterprise.id")
    employment_type_id: int = Field(foreign_key="employmenttype.id")

    users: list["User"] = Relationship(back_populates="careers", link_model=UserCareer)
    employment_type: EmploymentType | None = Relationship(back_populates="careers", sa_relationship_kwargs=dict(lazy="joined"))
    enterprise: Enterprise | None = Relationship(back_populates="careers", sa_relationship_kwargs=dict(lazy="joined"))

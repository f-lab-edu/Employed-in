import datetime

from sqlmodel import Field, SQLModel


class UserProfile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    profile_id:  int = Field(foreign_key="profile.id")


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
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    skill_id: int = Field(foreign_key="skill.id")


class Profile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=True, max_length=30)
    occupation: str = Field(nullable=True, max_length=30)
    personal_description: str = Field(nullable=True, max_length=255)
    country_id: int = Field(foreign_key="country.id")
    region: str = Field(nullable=True, max_length=50)


class Education(SQLModel, table=True):
    id: int = Field(primary_key=True)
    major: str = Field(max_length=50)
    start_time: datetime.datetime = Field()
    graduate_time: datetime.datetime = Field(nullable=True, default=None)
    grade: str = Field(nullable=True, max_length=10)
    description: str = Field(nullable=True, max_length=45)
    enterprise_id: int = Field(foreign_key="enterprise.id")


class Enterprise(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(max_length=255)
    enterprise_type_id: int = Field(foreign_key="enterprisetype.id")
    industry_id: int = Field(foreign_key="industry.id")
    country_id: int = Field(foreign_key="country.id")


class Career(SQLModel, table=True):
    id: int = Field(primary_key=True)
    position: str = Field(max_length=30)
    description: str = Field(nullable=True, default=None, max_length=255)
    start_time: datetime.datetime = Field()
    end_time: datetime.datetime = Field(nullable=True, default=None)
    enterprise_id: int = Field(foreign_key="enterprise.id")
    employment_type_id: int = Field(foreign_key="employmenttype.id")


class EnterpriseType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)
    degree_type: str = Field(nullable=True, default=None, max_length=20)


class Industry(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)


class Country(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)


class Skill(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=30)


class EmploymentType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=20)



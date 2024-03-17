import datetime

from sqlmodel import Field, SQLModel


class UserProfile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    personal_description: str = Field(nullable=True, max_length=255)
    language_id: int = Field(foreign_key="language.id")
    user_id: int = Field(foreign_key="user.id")
    skill_id:  int = Field(foreign_key="skill.id", nullable=True, default=None)


class Education(SQLModel, table=True):
    id: int = Field(primary_key=True)
    major: str = Field(max_length=50)
    start_time: datetime.datetime = Field()
    graduate_time: datetime.datetime = Field(nullable=True, default=None)
    grade: str = Field(nullable=True, max_length=10)
    description: str = Field(nullable=True, max_length=45)
    enterprise_id: int = Field(foreign_key="enterprise.id")
    userprofile_id: int = Field(foreign_key="userprofile.id")


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
    user_profile_id: int = Field(foreign_key="userprofile.id")
    skill_id: int = Field(foreign_key="skill.id")


class EnterpriseType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=100)
    degree_type: str = Field(nullable=True, default=None, max_length=20)


class Language(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=50)


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



import datetime

from sqlmodel import Field, SQLModel, Relationship

from .profile import UserSkill, UserCareer, UserEducation

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    email: str = Field(
        min_length=1, max_length=60, unique=True, default=None, index=True
    )
    phone_number: str = Field(nullable=True, default=None, max_length=25)
    password: str = Field(max_length=255)
    nickname: str = Field(nullable=True, default=None, max_length=10)
    is_admin: bool = Field(default=False)
    is_business: bool = Field(default=False)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    membership_id: int = Field(foreign_key="membership.id")

    skills: list["Skill"] = Relationship(back_populates="users", link_model=UserSkill)
    careers: list["Career"] = Relationship(back_populates="users", link_model=UserCareer)
    educations: list["Education"] = Relationship(back_populates="users", link_model=UserEducation)
    profiles: list["Profile"] = Relationship(back_populates="user")


class UserRelation(SQLModel, table=True):
    __tablename__ = "user_relation"

    id: int = Field(primary_key=True)
    follower: int = Field(foreign_key="user.id")
    followed: int = Field(foreign_key="user.id")


class Membership(SQLModel, table=True):
    __tablename__ = "membership"

    id: int = Field(primary_key=True)
    name: str = Field(max_length=10)

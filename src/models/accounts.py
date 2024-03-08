import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(min_length=1, max_length=60, unique=True, default=None)
    phone_number: str = Field(nullable=True, default=None, max_length=25)
    password: str = Field(max_length=255)
    nickname: str = Field(nullable=True, default=None, max_length=10)
    is_admin: bool = Field(default=None)
    is_business: bool = Field(default=None)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    membership_id: int = Field(foreign_key='membership.id')


class UserRelation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    follower: int = Field(foreign_key="user.id")
    followed: int = Field(foreign_key="user.id")


class Membership(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=10)

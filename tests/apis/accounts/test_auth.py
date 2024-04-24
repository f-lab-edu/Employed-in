import datetime
import os

import pytest
from fastapi import status
from httpx import AsyncClient
from jose import jwt
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.accounts import User
from src.models.repository import UserRepository
from src.service.accounts import UserService


@pytest.mark.asyncio
async def test_signup_successfully(client: AsyncClient, session: AsyncSession, mocker):
    hashed_password = mocker.patch.object(
        UserService, "hash_password", return_value="hashed"
    )

    test_user = User(
        id=None,
        email="unittest@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    new_user = mocker.patch.object(
        UserRepository,
        "create_user",
        return_value=test_user,
    )

    response = await client.post(
        url="/account/signup",
        json={
            "email": "unittest@test.com",
            "password": "Plain123!",
            "confirm_password": "Plain123!",
            "phone_number": "010-1111-1111",
            "membership_id": 1,
        },
    )

    token = jwt.encode(
        {
            "sub": "unittest@test.com",
            "exp": datetime.datetime.now() + datetime.timedelta(days=7),
        },
        os.getenv("SECRET_KEY"),
        algorithm="HS512",
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data == {"access_token": token}


@pytest.mark.asyncio
async def test_signup_registered_case(
    client: AsyncClient, session: AsyncSession, mocker
):
    user = mocker.patch.object(
        UserRepository,
        "get_user_by_email",
        return_value=User(
            id=None,
            email="test@test.com",
            password="hashed",
            nickname=None,
            phone_number="010-1111-1111",
            is_business=False,
            is_admin=False,
            created_at=datetime.datetime.now(),
            membership_id=1,
        ),
    )

    response = await client.post(
        url="/account/signup",
        json={
            "email": "test@test.com",
            "password": "Plain123!",
            "confirm_password": "Plain123!",
            "phone_number": "010-1111-1111",
            "membership_id": 1,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data == {"detail": "already registered"}


@pytest.mark.asyncio
async def test_login_successfully(client: AsyncClient, session: AsyncSession, mocker):
    user = mocker.patch.object(
        UserRepository,
        "get_user_by_email",
        return_value=User(
            id=1,
            email="test@test.com",
            password="hashed",
            nickname=None,
            phone_number="010-1111-1111",
            is_business=False,
            is_admin=False,
            created_at=datetime.datetime.now(),
            membership_id=1,
        ),
    )

    verify = mocker.patch.object(UserService, "verify_password", return_value=True)

    response = await client.post(
        url="/account/login", json={"email": "test@test.com", "password": "Plain123!"}
    )

    token = jwt.encode(
        {
            "sub": "test@test.com",
            "exp": datetime.datetime.now() + datetime.timedelta(days=7),
        },
        os.getenv("SECRET_KEY"),
        algorithm="HS512",
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {"access_token": token}


@pytest.mark.asyncio
async def test_login_no_user_case(client: AsyncClient, session: AsyncSession, mocker):
    response = await client.post(
        url="/account/login", json={"email": "nouser@test.com", "password": "Plain123!"}
    )

    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_login_wrong_password_case(
    client: AsyncClient, session: AsyncSession, mocker
):
    user = mocker.patch.object(
        UserRepository,
        "get_user_by_email",
        return_value=User(
            id=1,
            email="test@test.com",
            password="hashed",
            nickname=None,
            phone_number="010-1111-1111",
            is_business=False,
            is_admin=False,
            created_at=datetime.datetime.now(),
            membership_id=1,
        ),
    )

    verify = mocker.patch.object(UserService, "verify_password", return_value=False)

    response = await client.post(
        url="/account/login", json={"email": "test@test.com", "password": "Plain123!"}
    )

    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Invalid password"}
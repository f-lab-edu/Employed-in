import datetime
import os

import pytest
from fastapi import status
from httpx import AsyncClient
from jose import jwt
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.accounts import User
from src.service.accounts import UserService


@pytest.mark.asyncio
async def test_signup_successfully(client: AsyncClient, session: AsyncSession, mocker):
    hashed_password = mocker.patch.object(
        UserService, "hash_password", return_value="hashed"
    )

    new_user = mocker.patch.object(
        User,
        "create",
        return_value=User(
            id=None,
            email="test@test.com",
            password="hashed",
            created_at=datetime.datetime.now(),
            membership_id=1,
        ),
    )

    response = await client.post(
        url="/accounts/signup",
        json={
            "email": "test@test.com",
            "password": "plain",
            "confirmed_password": "plain",
            "membership_id": 1,
        },
    )

    hashed_password.assert_called_once_with(plain_password="plain")

    new_user.assert_called_once_with(
        email="test@test.com",
        password="hashed",
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    token = jwt.encode(
        {
            "sub": "test@test.com",
            "exp": datetime.datetime.now() + datetime.timedelta(days=7),
        },
        os.getenv("SECRET_KEY"),
        algorithm="HS512",
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data == token

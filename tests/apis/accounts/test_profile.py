import os
import datetime
import pytest

from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.accounts import User
from src.models.profile import Profile, Country
from src.models.repository import ProfileRepository, UserRepository
from src.service.accounts import UserService
from src.interfaces.permission import Auths


@pytest.mark.asyncio
async def test_create_profile_successfully(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    test_profile = Profile(
        name="test",
        occupation="test",
        personal_description="test",
        region="test",
        country_id=1,
        user_id=1
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profile_validation = mocker.patch.object(
        ProfileRepository, "profile_validation", return_value=True
    )

    mocker_new_profile = mocker.patch.object(
        ProfileRepository, "create_profile", return_value=test_profile
    )

    response = await client.post(
        url="/account/profile",
        headers={"Authorization" : "Bearer test"},
        json={
            "name" : "test",
            "occupation" : "test",
            "personal_description" : "test",
            "region" : "test",
            "country_id" : 1
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data == {
        "message" : "New profile created",
        "data" : {
            "name" :"test",
            "occupation" : "test",
            "personal_description" : "test",
            "region" : "test",
            "country_id" : 1,
            "user_id" : 1
                }
    }


@pytest.mark.asyncio
async def test_create_profile_auth_failure(client: AsyncClient, session: AsyncSession):
    response = await client.post(
        url="/account/profile",
        json={
            "name": "test",
            "occupation": "test",
            "personal_description": "test",
            "region": "test",
            "country_id": 1
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()

    assert data == {
        "detail" : "No auth credential"
    }


@pytest.mark.asyncio
async def test_profile_list_successfully(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mock_profiles = [
        (Profile(
            id=1,
            name="test",
            occupation="test",
            personal_description="test",
            region="test",
            country_id=1,
            user_id=1
        ), "South korea"),
        (Profile(
            id=2,
            name="test",
            occupation="test",
            personal_description="test",
            region="test",
            country_id=2,
            user_id=1
        ), "North korea"),
        (Profile(
            id=3,
            name="test",
            occupation="test",
            personal_description="test",
            region="test",
            country_id=3,
            user_id=1
        ), "International")
    ]

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profiles = mocker.patch.object(
        ProfileRepository, "filter_profile_by_user", return_value=mock_profiles
    )

    response = await client.get(
        url="/account/profiles",
        headers={"Authorization" : "Bearer test"},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == [
        {
            "id": 1,
            "name": "test",
            "occupation": "test",
            "personal_description": "test",
            "region": "test",
            "country_name": "South korea"

        },
        {
            "id": 2,
            "name": "test",
            "occupation": "test",
            "personal_description": "test",
            "region": "test",
            "country_name": "North korea"

        },
        {
            "id": 3,
            "name": "test",
            "occupation": "test",
            "personal_description": "test",
            "region": "test",
            "country_name": "International"

        }
    ]


@pytest.mark.asyncio
async def test_get_profile_successfully(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mock_profile = (Profile(
            id=1,
            name="Marx",
            occupation="Revolutionary",
            personal_description="test",
            region="test",
            country_id=1,
            user_id=1
        ), "International")

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profiles = mocker.patch.object(
        ProfileRepository, "get_profile_by_id", return_value=mock_profile
    )

    response = await client.get(
        url="/account/profiles/1",
        headers={"Authorization": "Bearer test"},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
            "id": 1,
            "name": "Marx",
            "occupation": "Revolutionary",
            "personal_description": "test",
            "region": "test",
            "country_name": "International"
        }


@pytest.mark.asyncio
async def test_get_profile_fail_invalid_id(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    response = await client.get(
        url="/account/profiles/999",
        headers={"Authorization": "Bearer test"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data == {"detail": "Invalid profile id"}


@pytest.mark.asyncio
async def test_update_profile_successfully(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mock_profile1 = (Profile(
        id=1,
        name="SiJun",
        occupation="Mafia",
        personal_description="Mansang",
        region="Uiju",
        country_id=1,
        user_id=1
    ), "Joseon")

    mock_profile2 = Profile(
        id=1,
        name="SiJun",
        occupation="Juseog",
        personal_description="Indomitable Revolutionary",
        region="Pyongyang",
        country_id=2,
        user_id=1
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profiles = mocker.patch.object(
        ProfileRepository, "get_profile_by_id", return_value=mock_profile1
    )

    mocker_new_profile = mocker.patch.object(
        ProfileRepository, "create_profile", return_value=mock_profile2
    )

    response = await client.patch(
        url="/account/profile",
        headers={"Authorization": "Bearer test"},
        json={
            "name": "SiJun",
            "occupation": "Juseog",
            "personal_description": "Indomitable Revolutionary",
            "region": "Pyongyang",
            "country_id": 2,
            "profile_id": 1
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data == {
        "message": "Profile updated",
        "data": {
            "id" : 1,
            "name": "SiJun",
            "occupation": "Juseog",
            "personal_description": "Indomitable Revolutionary",
            "region": "Pyongyang",
            "country_id": 2,
            "user_id": 1
        }
    }


@pytest.mark.asyncio
async def test_update_profile_fail_without_id(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    response = await client.patch(
        url="/account/profile",
        headers={"Authorization": "Bearer test"},
        json={
            "name": "SiJun",
            "occupation": "Juseog",
            "personal_description": "Indomitable Revolutionary",
            "region": "Pyongyang",
            "country_id": 2,
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data == {"detail": "profile id missed"}


@pytest.mark.asyncio
async def test_update_profile_fail_invalid_id(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    response = await client.patch(
        url="/account/profile",
        headers={"Authorization": "Bearer test"},
        json={
            "name": "SiJun",
            "occupation": "Juseog",
            "personal_description": "Indomitable Revolutionary",
            "region": "Pyongyang",
            "country_id": 2,
            "profile_id": 999999
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data == {"detail": "Invalid profile id"}


@pytest.mark.asyncio
async def test_delete_profile_successfully(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mock_profile = Profile(
        id=2,
        name="LeeGong",
        occupation="King",
        personal_description="Orphan",
        region="Hanseong",
        country_id=1,
        user_id=1
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profile = mocker.patch.object(
        ProfileRepository, "delete_profile", return_value=mock_profile
    )

    response = await client.delete(
        url="/account/profiles/2",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "message" : "Profile deleted",
        "data" : {
            "id": 2,
            "name": "LeeGong",
            "occupation": "King",
            "personal_description": "Orphan",
            "region": "Hanseong",
            "country_id": 1,
            "user_id": 1
        }
    }


@pytest.mark.asyncio
async def test_delete_profile_fail_invalid_id(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    response = await client.delete(
        url="/account/profiles/999",
        headers={"Authorization": "Bearer test"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data == {"detail": "Invalid profile id"}


@pytest.mark.asyncio
async def test_country_list_successfully(client: AsyncClient, session: AsyncSession, mocker):
    test_user = User(
        id=1,
        email="test@test.com",
        password="hashed",
        nickname=None,
        phone_number="010-1111-1111",
        is_business=False,
        is_admin=False,
        created_at=datetime.datetime.now(),
        membership_id=1,
    )

    test_countries = [
        Country(
            id=1,
            name="South Korea"
        ),
        Country(
            id=2,
            name="North Korea"
        )
    ]

    mocker_user = mocker.patch.object(
        Authentications, "basic_authentication", return_value=test_user
    )

    mocker_profiles = mocker.patch.object(
        ProfileRepository, "get_country_list", return_value=test_countries
    )

    response = await client.get(
        url="/account/countries",
        headers={"Authorization": "Bearer test"},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == [
        {
            "id": 1,
            "name": "South Korea"
        },
        {
            "id": 2,
            "name": "North Korea"
        }
    ]

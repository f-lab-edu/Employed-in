import os
import datetime
import pytest

from dateutil.relativedelta import relativedelta
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.engine.row import RowMapping

from src.models.accounts import User
from src.models.profile import Profile, Country, Skill, UserSkill, Career, UserCareer, Enterprise, EnterpriseType, EmploymentType, Education, UserEducation
from src.models.repository import AccountRepository
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
        profiles=[]
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

    mocker_new_profile = mocker.patch.object(
        AccountRepository, "add_object", return_value=test_profile
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
        profiles=[
        Profile(
            id=1,
            name="test",
            occupation="test",
            personal_description="test",
            region="test",
            country_id=1,
            user_id=1,
            country=Country(
        id=1,
        name="South korea"
    )
        ),
        Profile(
            id=2,
            name="test",
            occupation="test",
            personal_description="test",
            region="test",
            country_id=2,
            user_id=1,
            country=Country(
                id=2,
                name="North korea"
    )
        ),
        Profile(
            id=3,
            name="test",
            occupation="test",
            personal_description="test",
            region="test",
            country_id=3,
            user_id=1,
            country=Country(
                id=3,
                name="International"
            )
        )
    ]
    )


    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
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

    mock_profile = Profile(
            id=1,
            name="Marx",
            occupation="Revolutionary",
            personal_description="test",
            region="test",
            country_id=1,
            user_id=1,
            country=Country(
                id=1,
                name="International"
            )
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profiles = mocker.patch.object(
        AccountRepository, "get_obj_by_id", return_value=mock_profile
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

    mock_profile1 = Profile(
        id=1,
        name="SiJun",
        occupation="Mafia",
        personal_description="Mansang",
        region="Uiju",
        country_id=1,
        user_id=1,
        country=Country(
            id=1,
            name="Joseon"
        )
    )

    mock_profile2 = Profile(
        id=2,
        name="SiJun",
        occupation="Juseog",
        personal_description="Indomitable Revolutionary",
        region="Pyongyang",
        country_id=1,
        user_id=1,
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profiles = mocker.patch.object(
        AccountRepository, "get_obj_by_id", return_value=mock_profile1
    )

    mocker_new_profile = mocker.patch.object(
        AccountRepository, "add_object", return_value=mock_profile2
    )

    response = await client.patch(
        url="/account/profile",
        headers={"Authorization": "Bearer test"},
        json={
            "name": "SiJun",
            "occupation": "Juseog",
            "personal_description": "Indomitable Revolutionary",
            "region": "Pyongyang",
            "country_id": 1,
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
            "country_id": 1,
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

    mock_country = Country(
        id=1,
        name="Josun"
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profile = mocker.patch.object(
        AccountRepository, "get_obj_by_id", return_value=mock_profile
    )

    mocker_profile = mocker.patch.object(
        AccountRepository, "delete_object", return_value=mock_profile
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
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_profiles = mocker.patch.object(
        AccountRepository, "get_all_obj", return_value=test_countries
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


@pytest.mark.asyncio
async def test_register_exist_skill_successfully(client: AsyncClient, session: AsyncSession, mocker):
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
        skills=[]
    )

    test_skill = Skill(
        id=1,
        name="cemen"
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_relation = mocker.patch.object(
        AccountRepository, "add_object", return_valie=test_skill
    )

    response = await client.post(
        url="/account/skills",
        headers={"Authorization": "Bearer test"},
        json={
            "name": "cemen"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data == {
        "message": "Skill is registered"
    }


@pytest.mark.asyncio
async def test_register_new_skill_successfully(client: AsyncClient, session: AsyncSession, mocker):
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
        skills=[]
    )

    test_skill = Skill(
        id=1,
        name="cemen"
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_skill = mocker.patch.object(
        AccountRepository, "add_object", side_effects=[test_skill, test_user]
    )

    response = await client.post(
        url="/account/skills",
        headers={"Authorization": "Bearer test"},
        json={
            "id": 1,
            "name": "cemen"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data == {
        "message": "Skill is registered"
    }


@pytest.mark.asyncio
async def test_all_skill_list_successfully(client: AsyncClient, session: AsyncSession, mocker):
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

    test_skills = [
        Skill(
            id=1,
            name="test1"
        ),
        Skill(
            id=2,
            name="test2"
        ),
        Skill(
            id=3,
            name="test3"
        )
    ]

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_new_skill = mocker.patch.object(
        AccountRepository, "get_all_obj", return_value=test_skills
    )

    response = await client.get(
        url="/account/skills",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == [
        {
            "id": 1,
            "name": "test1"
        },
        {
            "id": 2,
            "name": "test2"
        },
        {
            "id": 3,
            "name": "test3"
        }
    ]


@pytest.mark.asyncio
async def test_registered_skill_list_successfully(client: AsyncClient, session: AsyncSession, mocker):
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
        skills=[
            Skill(
                id=1,
                name="test1"
            ),
            Skill(
                id=2,
                name="test2"
            ),
            Skill(
                id=3,
                name="test3"
            )
        ]
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    response = await client.get(
        url="/account/skills/registered",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == [
        {
            "id": 1,
            "name": "test1"
        },
        {
            "id": 2,
            "name": "test2"
        },
        {
            "id": 3,
            "name": "test3"
        }
    ]


@pytest.mark.asyncio
async def test_registered_skill_delete_successfully(client: AsyncClient, session: AsyncSession, mocker):
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
        skills=[
            Skill(
                id=1,
                name="test1"
            ),
            Skill(
                id=2,
                name="test2"
            ),
            Skill(
                id=3,
                name="test3"
            )
        ]
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_relation = mocker.patch.object(
        AccountRepository, "add_object", return_value=test_user
    )

    response = await client.delete(
        url="/account/skills/registered/2",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "message": "Skill is deleted"
    }


@pytest.mark.asyncio
async def test_register_career_successfully(client: AsyncClient, session: AsyncSession, mocker):
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
        careers=[]
    )

    start_date = datetime.datetime.now().date() - relativedelta(months=6)

    end_date = datetime.datetime.now().date() + relativedelta(months=6)

    test_career = Career(
        id=1,
        position="Intern",
        description="Lab Dog",
        start_time=start_date,
        end_time=end_date,
        enterprise_id=1,
        employment_type_id=1
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_relation = mocker.patch.object(
        AccountRepository, "add_object", side_effects=[test_career, test_user]
    )

    response = await client.post(
        url="/account/careers",
        headers={"Authorization": "Bearer test"},
        json={
            "position": "Intern",
            "description": "Lab Dog",
            "start_time": start_date.strftime("%Y-%m-%d"),
            "end_time": end_date.strftime("%Y-%m-%d"),
            "enterprise_id": 1,
            "employment_type_id": 1
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data == {
        "message": "Career is registered"
    }


@pytest.mark.asyncio
async def test_registered_career_list_successfully(client: AsyncClient, session: AsyncSession, mocker):
    date = datetime.datetime.now().date()

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
        careers=[
           Career(
                id=1,
                position="Intern",
                description="Lab Dog",
                start_time=date - relativedelta(years=3),
                end_time=date - relativedelta(years=2),
                enterprise_id=1,
                employment_type_id=1,
                employment_type=EmploymentType(
                    id=1,
                    name="Intern"
                ),
                enterprise=Enterprise(
                    id=1,
                    name="test_ent"
                )
            ),
            Career(
                id=2,
                position="Manager",
                description="Lab Dog Manager",
                start_time=date - relativedelta(years=2),
                end_time=date - relativedelta(years=1),
                enterprise_id=1,
                employment_type_id=2,
                employment_type=EmploymentType(
                    id=2,
                    name="Manager"
                ),
                enterprise=Enterprise(
                    id=1,
                    name="test_ent"
                )
            ),
            Career(
                id=3,
                position="Emperor",
                description="Master of Mankind",
                start_time=date - relativedelta(years=1),
                end_time=None,
                enterprise_id=1,
                employment_type_id=3,
                employment_type=EmploymentType(
                    id=3,
                    name="Emperor"
                ),
                enterprise=Enterprise(
                    id=1,
                    name="test_ent"
                )

            )
        ]
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    response = await client.get(
        url="/account/careers",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == [
        {
            "id": 1,
            "position": "Intern",
            "description": "Lab Dog",
            "start_time": (date - relativedelta(years=3)).strftime("%Y-%m-%d"),
            "end_time": (date - relativedelta(years=2)).strftime("%Y-%m-%d"),
            "employment_type_id" : 1,
            "employment_type_name": "Intern",
            "enterprise_id": 1,
            "enterprise_name": "test_ent"
        },
        {
            "id": 2,
            "position": "Manager",
            "description": "Lab Dog Manager",
            "start_time": (date - relativedelta(years=2)).strftime("%Y-%m-%d"),
            "end_time": (date - relativedelta(years=1)).strftime("%Y-%m-%d"),
            "employment_type_id": 2,
            "employment_type_name": "Manager",
            "enterprise_id": 1,
            "enterprise_name": "test_ent"
        },
        {
            "id": 3,
            "position": "Emperor",
            "description": "Master of Mankind",
            "start_time": (date - relativedelta(years=1)).strftime("%Y-%m-%d"),
            "end_time": None,
            "employment_type_id": 3,
            "employment_type_name": "Emperor",
            "enterprise_id": 1,
            "enterprise_name": "test_ent"
        }
    ]


@pytest.mark.asyncio
async def test_registered_career_delete_successfully(client: AsyncClient, session: AsyncSession, mocker):

    date = datetime.datetime.now().date()

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
        careers=[
            Career(
                id=1,
                position="Intern",
                description="Lab Dog",
                start_time=date - relativedelta(years=3),
                end_time=date - relativedelta(years=2),
                enterprise_id=1,
                employment_type_id=1,
                employment_type=EmploymentType(
                    id=1,
                    name="Intern"
                ),
                enterprises=Enterprise(
                    id=1,
                    name="test_ent"
                )
            )
        ]
    )

    test_career = Career(
                id=1,
                position="Intern",
                description="Lab Dog",
                start_time=date - relativedelta(years=3),
                end_time=date - relativedelta(years=2),
                enterprise_id=1,
                employment_type_id=1,
                employment_type=EmploymentType(
                    id=1,
                    name="Intern"
                ),
                enterprises=Enterprise(
                    id=1,
                    name="test_ent"
                )
            )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_career = mocker.patch.object(
        AccountRepository, "get_obj_by_id", return_value=test_career
    )

    mocker_deletion = mocker.patch.object(
        AccountRepository, "delete_object", return_value=test_career
    )

    response = await client.delete(
        url="/account/careers/1",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "message": "Career is deleted"
    }


@pytest.mark.asyncio
async def test_register_education_successfully(client: AsyncClient, session: AsyncSession, mocker):
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
        educations=[]
    )

    start_date = datetime.datetime.now().date() - relativedelta(months=6)

    end_date = datetime.datetime.now().date() + relativedelta(months=6)

    test_education = Education(
        id=1,
        major="Sociology",
        start_time=start_date,
        graduate_time=end_date,
        grade="4.0",
        degree_type="Bachelor",
        description="Lab Dog",
        enterprise_id=1,
        enterprise=Enterprise(
            id=1,
            name="test_ent"
        )
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    mocker_relation = mocker.patch.object(
        AccountRepository, "add_object", side_effect=[test_education, test_user]
    )

    response = await client.post(
        url="/account/educations",
        headers={"Authorization": "Bearer test"},
        json={
            "major": "Sociology",
            "description": "Lab Dog",
            "start_time": start_date.strftime("%Y-%m-%d"),
            "graduate_time": end_date.strftime("%Y-%m-%d"),
            "grade" : "4.0",
            "degree_type" : "Bachelor",
            "enterprise_id": 1
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data == {
        "message": "Education is registered"
    }


@pytest.mark.asyncio
async def test_registered_education_list_successfully(client: AsyncClient, session: AsyncSession, mocker):
    date = datetime.datetime.now().date()

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
        educations=[
            Education(
                id=1,
                major="Sociology",
                description="Lab Dog",
                start_time=date - relativedelta(years=3),
                graduate_time=date,
                grade="4.0",
                degree_type="Bachelor",
                enterprise=Enterprise(
                    id=1,
                    name="IOTS",
                )
            ),
            Education(
                id=2,
                major="Sociology",
                description="Lab Dog",
                start_time=date,
                graduate_time=None,
                grade="4.0",
                degree_type="Master",
                enterprise=Enterprise(
                    id=1,
                    name="IOTS",
                )
            )
        ]
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    response = await client.get(
        url="/account/educations",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == [
        {
            "id": 1,
            "major": "Sociology",
            "start_time": (date - relativedelta(years=3)).strftime("%Y-%m-%d"),
            "graduate_time": date.strftime("%Y-%m-%d"),
            "degree_type": "Bachelor",
            "grade": "4.0",
            "description": "Lab Dog",
            "enterprise_id": 1,
            "enterprise_name": "IOTS",
        },
        {
            "id": 2,
            "major": "Sociology",
            "start_time": date.strftime("%Y-%m-%d"),
            "graduate_time": None,
            "degree_type": "Master",
            "grade": "4.0",
            "description": "Lab Dog",
            "enterprise_id": 1,
            "enterprise_name": "IOTS",
        }
    ]


@pytest.mark.asyncio
async def test_registered_education_delete_successfully(client: AsyncClient, session: AsyncSession, mocker):
    date = datetime.datetime.now().date()

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
        educations=[
            Education(
                id=1,
                major="Sociology",
                description="Lab Dog",
                grade="4.0",
                degree_type="Bachelor",
                start_time=date - relativedelta(years=3),
                graduate_time=date - relativedelta(years=2),
                enterprise_id=1,
            )
        ]
    )

    mocker_user = mocker.patch.object(
        Auths, "basic_authentication", return_value=test_user
    )

    test_education = Education(
        id=1,
        major="Sociology",
        description="Lab Dog",
        grade="4.0",
        degree_type="Bachelor",
        start_time=date - relativedelta(years=3),
        graduate_time=date - relativedelta(years=2),
        enterprise_id=1,
            )

    mocker_relation = mocker.patch.object(
        AccountRepository, "get_obj_by_id", return_value=test_education
    )

    mocker_relation = mocker.patch.object(
        AccountRepository, "delete_object", return_value=test_education
    )

    response = await client.delete(
        url="/account/educations/1",
        headers={"Authorization": "Bearer test"}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "message": "Education is deleted"
    }

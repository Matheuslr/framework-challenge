import json

import pytest
from rest_framework.test import APIClient

from user.services import UserDataClass


@pytest.fixture
def user():
    user_dc = UserDataClass(
        first_name="Joe",
        last_name="Doe",
        email="joedoe@test.com",
        password="password123",
    )

    UserDataClass.create_user(user_dc=user_dc)

    return user_dc


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    payload = json.dumps(dict(email=user.email, password=user.password))
    client.post("/api/login/", payload, content_type="application/json")

    return client

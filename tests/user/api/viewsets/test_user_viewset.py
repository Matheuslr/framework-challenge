import json
from http.cookies import SimpleCookie

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from user.services import UserDataClass


@pytest.mark.django_db
def test_should_register_user(client):
    payload = dict(
        first_name="Joe",
        last_name="Doe",
        email="joedoetest@test.com",
        password="password123",
    )

    response = client.post(
        "/api/register/", json.dumps(payload), content_type="application/json"
    )

    data = response.data

    assert response.status_code == HTTP_201_CREATED
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db
def test_should_login_user(client, user: "UserDataClass"):
    payload = dict(email=user.email, password=user.password)
    response = client.post(
        "/api/login/", json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_should_not_login_without_email_on_payload(
    client, user: "UserDataClass"
):
    payload = dict(password=user.password)
    response = client.post(
        "/api/login/", json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    response.data[
        "detail"
    ] == "ErrorDetail(string='Missing email', code='authentication_failed"


@pytest.mark.django_db
def test_should_not_login_without_password_on_payload(
    client, user: "UserDataClass"
):
    payload = dict(email=user.email)
    response = client.post(
        "/api/login/", json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    response.data[
        "detail"
    ] == "ErrorDetail(string='Missing password', code='authentication_failed"


@pytest.mark.django_db
def test_should_not_login_with_wrong_email(client, user: "UserDataClass"):
    payload = dict(email="wrong_email@gmail.com", password=user.password)
    response = client.post(
        "/api/login/", json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    response.data[
        "detail"
    ] == "ErrorDetail(string='Invalid Credentials',\
         code='authentication_failed"


@pytest.mark.django_db
def test_should_not_login_with_wrong_password(client, user: "UserDataClass"):
    payload = dict(email=user.email, password="wrong-password")
    response = client.post(
        "/api/login/", json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    response.data[
        "detail"
    ] == "ErrorDetail(string='Invalid Credentials',\
         code='authentication_failed')"


@pytest.mark.django_db
def test_should_user_me(auth_client, user: "UserDataClass"):

    response = auth_client.get("/api/me/")

    data = response.data

    assert response.status_code == HTTP_200_OK
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name
    assert data["email"] == user.email
    assert "password" not in data


@pytest.mark.django_db
def test_should_not_access_user_me_route_unauthenticated(
    client, user: "UserDataClass"
):

    response = client.get("/api/me/")

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_should_not_access_authenticate_only_route_with_empty_cookie(
    auth_client, user: "UserDataClass"
):

    auth_client.cookies = SimpleCookie("")
    response = auth_client.get("/api/me/")

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_should_not_access_user_me_route_with_wrong_token(
    auth_client, user: "UserDataClass"
):

    auth_client.cookies = SimpleCookie({"jwt": "wrong_cookie"})
    response = auth_client.get("/api/me/")

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_should_user_logout(auth_client, user: "UserDataClass"):

    response = auth_client.post("/api/logout/")

    assert response.status_code == HTTP_200_OK

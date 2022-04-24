from unittest.mock import Mock, patch

import pytest
from django import http
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE


class TestJsonPlaceHolderViewset:
    payload = [
        {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": False,
        },
        {
            "userId": 1,
            "id": 2,
            "title": "quis ut nam facilis et officia qui",
            "completed": False,
        },
        {
            "userId": 1,
            "id": 3,
            "title": "fugiat veniam minus",
            "completed": False,
        },
        {"userId": 1, "id": 4, "title": "et porro tempora", "completed": True},
        {
            "userId": 1,
            "id": 5,
            "title": "laboriosam mollitia et enim quasi adipisci quia provident illum",
            "completed": False,
        },
        {
            "userId": 1,
            "id": 6,
            "title": "qui ullam ratione quibusdam voluptatem quia omnis",
            "completed": False,
        },
        {
            "userId": 1,
            "id": 7,
            "title": "illo expedita consequatur quia in",
            "completed": False,
        },
        {
            "userId": 1,
            "id": 8,
            "title": "quo adipisci enim quam ut ab",
            "completed": True,
        },
        {
            "userId": 1,
            "id": 9,
            "title": "molestiae perspiciatis ipsa",
            "completed": False,
        },
        {
            "userId": 1,
            "id": 10,
            "title": "illo est ratione doloremque quia maiores aut",
            "completed": True,
        },
    ]

    expected_response = [
        {"id": 1, "title": "delectus aut autem"},
        {"id": 2, "title": "quis ut nam facilis et officia qui"},
        {"id": 3, "title": "fugiat veniam minus"},
        {"id": 4, "title": "et porro tempora"},
        {"id": 5, "title": "laboriosam mollitia et enim quasi adipisci quia provident illum"},
    ]

    @pytest.mark.django_db
    def test_should_get_expected_result(self, auth_client):
        with patch(
            "json_placeholder.api.viewsets.json_placeholder_viewset.requests.get"
        ) as mock_get:

            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = self.payload.copy()
            response = auth_client.get("/api/app/json-placeholder/")
            data = response.json()
            assert response.status_code == HTTP_200_OK
            assert data == self.expected_response

    @pytest.mark.django_db
    def test_should_return_error_when_external_api_is_unavailiable(
        self, auth_client
    ):
        with patch(
            "json_placeholder.api.viewsets.json_placeholder_viewset.requests.get"
        ) as mock_get:

            mock_get.return_value.status_code = 503
            mock_get.return_value.json.return_value = self.payload.copy()
            response = auth_client.get("/api/app/json-placeholder/")
            data = response.json()
            assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
            assert data["error"]["reason"] == "Unavaliable external service"

    @pytest.mark.django_db
    def test_should_return_error_when_request_break(self, auth_client):
        with patch(
            "json_placeholder.api.viewsets.json_placeholder_viewset.requests.get"
        ) as mock_get:

            mock_get.return_value.status_code = 404
            mock_get.side_effect = http.Http404("error")
            response = auth_client.get("/api/app/json-placeholder/")
            data = response.json()
            assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
            assert data["error"]["reason"] == "error"

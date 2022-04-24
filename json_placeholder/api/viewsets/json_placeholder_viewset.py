import os

import requests
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from framework_api.helpers import error_logging, info_logging
from json_placeholder.api.serializers.json_placeholder_serialize import (
    JsonPlaceholderSerializer,
)
from user.authentication import CustomUserAuthentication


class JsonPlaceholderViewset(views.APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        json_placeholder_api_url = os.getenv("API_URL")
        try:
            api_response = requests.get(json_placeholder_api_url)
        except Exception as err:
            error_logging(data=err, status_code=503)
            return Response(
                {"error": {"reason": str(err)}},
                status=HTTP_503_SERVICE_UNAVAILABLE,
            )
        if api_response.status_code is not HTTP_200_OK:
            error_logging(data="Unavaliable external service", status_code=503)
            return Response(
                {"error": {"reason": "Unavaliable external service"}},
                status=HTTP_503_SERVICE_UNAVAILABLE,
            )

        expected_list = [
            {"id": item.get("id"), "title": item.get("title")}
            for item in api_response.json()[:5]
        ]

        result = JsonPlaceholderSerializer(expected_list, many=True).data
        info_logging(
            data=str(api_response.json()),
            status_code=api_response.status_code,
        )
        return Response(result, status=HTTP_200_OK)

import os

import requests
from rest_framework import views
from rest_framework.response import Response

from app.api.serializers.json_placeholder_serialize import (
    JsonPlaceholderSerializer,
)  # no qa


class JsonPlaceholderSerialize(views.APIView):
    def get(self, request):
        json_placeholder_api_url = os.getenv("API_URL")

        api_response = requests.get(json_placeholder_api_url).json()

        expected_list = api_response[:5]

        result = JsonPlaceholderSerializer(expected_list, many=True).data
        return Response(result)

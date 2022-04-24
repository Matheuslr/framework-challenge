"""
isort:skip_file
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from framework_api.helpers import info_logging
from user.api.serializers.user_serialize import (
    UserLogoutSerializerRequest,
    UserRegisterSerializerRequest,
    UserRegisterSerializerResponse,
    UserSerializer,
)
from user.authentication import CustomUserAuthentication
from user.services import UserDataClass as service


class RegisterViewset(views.APIView):
    permission_classes = (AllowAny,)
    description = "a route to register users"

    @swagger_auto_schema(
        operation_description=description,
        request_body=UserRegisterSerializerRequest,
        responses={201: UserRegisterSerializerResponse(many=True)},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.insatnce = service.create_user(user_dc=data)
        info_logging(data=(serializer.data))

        return Response(data=serializer.data, status=HTTP_201_CREATED)


class LoginViewset(views.APIView):

    permission_classes = (AllowAny,)
    description = "a route to login users"

    @swagger_auto_schema(
        operation_description=description,
        request_body=UserRegisterSerializerResponse,
        responses={204: {}},
    )
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email:
            raise exceptions.AuthenticationFailed("Missing email")
        if not password:
            raise exceptions.AuthenticationFailed("Missing password")

        user = service.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = service.create_token(user_id=user.id)

        resp = Response(status=HTTP_204_NO_CONTENT)

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserViewSet(views.APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    description = "a route to retrive info from logged user"

    @swagger_auto_schema(
        operation_description=description,
        responses={200: UserLogoutSerializerRequest(many=True)},
    )
    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data, status=HTTP_200_OK)


class LogoutApi(views.APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    description = "a route to logout users"

    @swagger_auto_schema(
        operation_description=description,
        responses={200: UserLogoutSerializerRequest(many=True)},
    )
    def post(self, request):
        resp = Response(status=HTTP_200_OK)
        resp.delete_cookie("jwt")
        resp.data = {"message": "goodbye!"}

        return resp

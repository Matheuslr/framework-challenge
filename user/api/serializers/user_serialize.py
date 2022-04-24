from rest_framework import serializers

from user.services import UserDataClass


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_internal_value(self, data):

        data = super().to_internal_value(data)

        return UserDataClass(**data)


class UserRegisterSerializerResponse(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()


class UserRegisterSerializerRequest(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


class UserLoginSerializerRequest(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserLogoutSerializerRequest(serializers.Serializer):
    message = serializers.CharField()

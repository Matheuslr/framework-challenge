import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from framework_api.helpers import error_logging
from user.models import User


class CustomUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=["HS256"]
            )  # no qa
        except Exception:
            error_logging(data="Unathorized user", status_code=401)
            raise AuthenticationFailed("Unathorized")

        user = User.objects.filter(id=payload["id"]).first()

        return (user, None)

import dataclasses
from datetime import datetime, timedelta

import jwt

from framework_api.helpers import info_logging
from framework_api.settings import JWT_SECRET
from user.models import User


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id,
        )

    def create_user(user_dc: "UserDataClass") -> "UserDataClass":

        instance = User(
            first_name=user_dc.first_name,
            last_name=user_dc.last_name,
            email=user_dc.email,
        )

        if user_dc.password is not None:
            instance.set_password(user_dc.password)

        instance.save()
        return UserDataClass.from_instance(instance)

    def user_email_selector(email: str) -> "User":
        user = User.objects.filter(email=email).first()

        return user

    def create_token(user_id: int) -> str:
        payload = dict(
            id=user_id,
            exp=datetime.utcnow() + timedelta(hours=24),
            iat=datetime.utcnow(),
        )

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return token

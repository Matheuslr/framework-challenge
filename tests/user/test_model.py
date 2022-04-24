import pytest
from django.contrib.auth import get_user_model

from user.models import User, UserManager


class TestUserMolde:
    payload = dict(
        first_name="Joe",
        last_name="Doe",
        email="joedoetest@test.com",
        password="password123",
    )

    User = get_user_model()

    @pytest.mark.django_db
    def test_should_create_usermanager_create_user(self):
        user = User.objects.create_user(**self.payload)

        user.first_name == self.payload["first_name"]
        user.last_name == self.payload["last_name"]
        user.email == self.payload["email"]
        user.password == self.payload["password"]

    @pytest.mark.django_db
    def test_should_create_usermanager_create_super_user(self):
        user = User.objects.create_superuser(**self.payload)

        user.first_name == self.payload["first_name"]
        user.last_name == self.payload["last_name"]
        user.email == self.payload["email"]
        user.password == self.payload["password"]
        user.is_staff is True
        user.is_superuser is True

    @pytest.mark.django_db
    def test_should_not_create_usermanager_without_email(self):
        with pytest.raises(ValueError):
            temp_payload = self.payload.copy()
            temp_payload["email"] = None
            User.objects.create_superuser(**temp_payload)

    @pytest.mark.django_db
    def test_should_not_create_usermanager_without_first_name(self):
        with pytest.raises(ValueError):
            temp_payload = self.payload.copy()
            temp_payload["first_name"] = None
            User.objects.create_superuser(**temp_payload)

    @pytest.mark.django_db
    def test_should_not_create_usermanager_without_last_name(self):
        with pytest.raises(ValueError):
            temp_payload = self.payload.copy()
            temp_payload["last_name"] = None
            User.objects.create_superuser(**temp_payload)

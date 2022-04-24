"""
isort:skip_file
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from user.api.viewsets.user_viewset import (
    LoginViewset,
    LogoutApi,
    RegisterViewset,
    UserViewSet,
)

router = DefaultRouter()

urlpatterns = [
    path("register/", RegisterViewset.as_view(), name="register"),
    path("login/", LoginViewset.as_view(), name="login"),
    path("logout/", LogoutApi.as_view(), name="logout"),
    path("me/", UserViewSet.as_view(), name="me"),
]

urlpatterns += router.urls

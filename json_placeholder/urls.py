from django.urls import path
from rest_framework.routers import DefaultRouter

from json_placeholder.api.viewsets.json_placeholder_viewset import (
    JsonPlaceholderViewset,
)

router = DefaultRouter()

urlpatterns = [path("json-placeholder/", JsonPlaceholderViewset.as_view())]

urlpatterns += router.urls

from django.urls import path, include
from .viewsets import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", CommentViewSet, basename="comment")
urlpatterns = [
    path("", include(router.urls)),
]

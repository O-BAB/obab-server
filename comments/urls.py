from django.urls import path
from .viewsets import CommentCreateAPIView, CommentUpdateDeleteAPIView


urlpatterns = [
    path("", CommentCreateAPIView.as_view(), name="comments-create"),
    path("<int:id>/", CommentUpdateDeleteAPIView.as_view(), name="comments-updatedelete"),
]

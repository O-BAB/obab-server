from django.urls import path, include

from users.views import UserInfoViews

urlpatterns = [
    path("", UserInfoViews.as_view(), name="userinfo"),
]

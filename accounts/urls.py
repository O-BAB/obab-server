from rest_framework.routers import SimpleRouter
from rest_framework.urls import path

from accounts.social_login import (
    GoogleCallbackView,
    GoogleLoginToDjango,
    GoogleLoginView,
    KakaoCallbackView,
    KakaoLoginToDjango,
    KakaoLoginView,
    NaverCallbackView,
    NaverLoginToDjango,
    NaverLoginView,
)

from .viewsets import RecipeBookmarkList, RecipeCommentList, RecipeWriteList, UserViewSet

router = SimpleRouter(trailing_slash=False)


social_url = [
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao_login"),
    path("kakao/callback/", KakaoCallbackView.as_view(), name="kakao_callback"),
    path("kakao/login/finish/", KakaoLoginToDjango.as_view(), name="kakao_login_to_django"),
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("google/callback/", GoogleCallbackView.as_view(), name="google_callback"),
    path("google/login/finish/", GoogleLoginToDjango.as_view(), name="google_login_to_django"),
    path("naver/login/", NaverLoginView.as_view(), name="naver_login"),
    path("naver/callback/", NaverCallbackView.as_view(), name="naver_callback"),
    path("naver/login/finish/", NaverLoginToDjango.as_view(), name="naver_login_to_django"),
]

login_url = [
    path("register/", UserViewSet.as_view({"post": "create"})),
    path("userinfo/<int:pk>", UserViewSet.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})),
    path("login/", UserViewSet.as_view({"post": "login"})),
    path("users/logout", UserViewSet.as_view({"get": "logout"})),
]

urlpatterns = [
    path("userinfo/bookmark", RecipeBookmarkList.as_view({"get": "list"}), name="user-bookmark-list"),
    path("userinfo/write", RecipeWriteList.as_view({"get": "list"}), name="user-write-list"),
    path("userinfo/comment", RecipeCommentList.as_view({"get": "list"}), name="user-comments-list"),
    *social_url,
    *login_url,
]

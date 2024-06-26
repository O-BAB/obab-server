from django.urls import path

from accounts.social_login import (
    GoogleLoginView,
    GoogleCallbackView,
    GoogleLoginToDjango,
    KakaoLoginView,
    KakaoCallbackView,
    KakaoLoginToDjango,
    NaverLoginView,
    NaverCallbackView,
    NaverLoginToDjango,
)
from .views import UserInfoViews, RegisterView, LoginView, TokenRefreshView

social_url = [
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao_login"),
    path("kakao/callback/", KakaoCallbackView.as_view(), name="kakao_callback"),
    path(
        "kakao/login/finish/",
        KakaoLoginToDjango.as_view(),
        name="kakao_login_to_django",
    ),
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("google/callback/", GoogleCallbackView.as_view(), name="google_callback"),
    path(
        "google/login/finish/",
        GoogleLoginToDjango.as_view(),
        name="google_login_to_django",
    ),
    path("naver/login/", NaverLoginView.as_view(), name="naver_login"),
    path("naver/callback/", NaverCallbackView.as_view(), name="naver_callback"),
    path(
        "naver/login/finish/",
        NaverLoginToDjango.as_view(),
        name="naver_login_to_django",
    ),
]

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("userinfo/", UserInfoViews.as_view(), name="userinfo"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    *social_url,
]

from django.urls import path

from accounts.social_views.kakao_login import (
    KakaoLoginView,
    KakaoCallbackView,
    KakaoLoginToDjango,
)

from accounts.social_views.google_login import (
    GoogleLoginView,
    GoogleCallbackView,
    GoogleLoginToDjango,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
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

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

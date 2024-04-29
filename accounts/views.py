import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from dj_rest_auth.registration.views import SocialLoginView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from accounts.models import User
from accounts.tokens import TokenResponseSerializer


class Constants:
    BASE_URL = getattr(settings, "BASE_URL")

    # kakao
    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_CALLBACK_URI = f"http://localhost:3000/kakao"

    # google
    GOOGLE_CALLBACK_URI = f"http://localhost:3000/google"
    GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    GOOGLE_SCOPE = " ".join(
        [
            "https://www.googleapis.com/auth/userinfo.email",
        ]
    )
    # naver
    NAVER_CALLBACK_URI = f"http://localhost:3000/naver"
    NAVER_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_NAVER_SECRET")

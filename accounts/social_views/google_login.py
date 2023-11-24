from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import requests
from accounts.models import User
from accounts.serializers import TokenResponseSerializer
from rest_framework.response import Response
from accounts.views import Constants
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    schema = None

    def get(self, request):
        return redirect(
            f"https://accounts.google.com/o/oauth2/v2/auth?client_id={Constants.GOOGLE_CLIENT_ID}"
            f"&response_type=code&redirect_uri={Constants.GOOGLE_CALLBACK_URI}&scope={Constants.GOOGLE_SCOPE}"
        )


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="구글 로그인 콜백",
        tags=["로그인"],
        parameters=[
            OpenApiParameter(
                name="code",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="구글에서 반환한 인증 코드",
            ),
        ],
    )
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        GOOGLE_CLIENT_ID = Constants.GOOGLE_CLIENT_ID
        GOOGLE_CLIENT_SECRET = Constants.GOOGLE_CLIENT_SECRET
        GOOGLE_CALLBACK_URI = Constants.GOOGLE_CALLBACK_URI
        code = request.GET.get("code")
        state = Constants.STATE

        token_req = requests.post(
            f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}"
            f"&client_secret={GOOGLE_CLIENT_SECRET}&code={code}"
            f"&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}"
            f"&state={state}"
        )
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get("error") == "invalid_request":
                return redirect(f"{BASE_URL}api/v1/accounts/google/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get("access_token")

        email_req = requests.get(
            f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
        )
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return JsonResponse(
                {"error": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
            )
        email_req_json = email_req.json()
        email = email_req_json.get("email")
        if not email:
            return JsonResponse(
                {"error": "email not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)

            if social_user.provider != "google":
                return JsonResponse(
                    {"err_msg": "no matching social type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {"access_token": access_token, "code": code}

            accept = requests.post(
                f"{BASE_URL}api/v1/accounts/google/login/finish/", data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signin"}, status=accept_status
                )
            serializer = TokenResponseSerializer(user)
            data = serializer.to_representation(serializer)
            res = Response(
                data,
                status=status.HTTP_200_OK,
            )
            return res

        except User.DoesNotExist:
            data = {"access_token": access_token, "code": code}
            accept = requests.post(
                f"{BASE_URL}api/v1/accounts/google/login/finish/", data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signup"}, status=accept_status
                )
            user = User.objects.get(email=email)
            serializer = TokenResponseSerializer(user)
            data = serializer.to_representation(serializer)
            res = Response(
                data,
                status=status.HTTP_200_OK,
            )
            return res


class GoogleLoginToDjango(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = Constants.GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    schema = None

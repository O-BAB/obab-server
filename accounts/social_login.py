import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.models import User
from core.constants import Constants
from core.responses import Response
from core.tokens import CustomJWTAuthentication

# ==================================================================== #
#                          구글 소셜로그인                                 #
# ==================================================================== #


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

    @swagger_auto_schema(
        operation_id="구글 로그인 콜백",
        operation_description="구글에서 반환한 인증 코드를 넣으면, 회원가입 or 로그인 후 서버 토큰 리턴\n"
        "닉네임이 없으면 message를 True 반환\n"
        "True면 닉네임, 프로필, 이름, 한줄 소개 업데이트",
        tags=["소셜 로그인"],
        manual_parameters=[
            openapi.Parameter(
                "code", in_=openapi.IN_QUERY, description="구글에서 반환한 인증 코드", type=openapi.TYPE_STRING, required=True
            )
        ],
    )
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        GOOGLE_CLIENT_ID = Constants.GOOGLE_CLIENT_ID
        GOOGLE_CLIENT_SECRET = Constants.GOOGLE_CLIENT_SECRET
        GOOGLE_CALLBACK_URI = Constants.GOOGLE_CALLBACK_URI
        code = request.GET.get("code")
        state = "random_string"

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
                return redirect(f"{BASE_URL}accounts/google/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get("access_token")

        email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return JsonResponse({"error": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST)
        email_req_json = email_req.json()
        email = email_req_json.get("email")
        if not email:
            return JsonResponse({"error": "email not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)

            if social_user.provider != "google":
                return JsonResponse({"err_msg": "no matching social type"}, status=status.HTTP_400_BAD_REQUEST)
            data = {"access_token": access_token, "code": code}

            accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
            token = CustomJWTAuthentication.create_token(user)
            res = Response(data=token)
            return res

        except User.DoesNotExist:
            data = {"access_token": access_token, "code": code}
            accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
            user = User.objects.get(email=email)
            token = CustomJWTAuthentication.create_token(user)
            res = Response(data=token)
            return res


class GoogleLoginToDjango(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = Constants.GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    schema = None


# ==================================================================== #
#                           네이버 소셜로그인                              #
# ==================================================================== #


class NaverLoginView(APIView):
    permission_classes = [AllowAny]
    schema = None

    def get(self, request):
        state = "random_string"
        return redirect(
            f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={Constants.NAVER_CLIENT_ID}"
            f"&state={state}&redirect_uri={Constants.NAVER_CALLBACK_URI}"
        )


class NaverCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="네이버 로그인 콜백",
        operation_description="네이버에서 반환한 인증 코드를 넣으면, 회원가입 or 로그인 후 서버 토큰 리턴\n"
        "닉네임이 없으면 message를 True 반환\n"
        "True면 닉네임, 프로필, 이름, 한줄 소개 업데이트",
        tags=["소셜 로그인"],
        manual_parameters=[
            openapi.Parameter(
                "code", in_=openapi.IN_QUERY, description="네이버에서 반환한 인증 코드", type=openapi.TYPE_STRING, required=True
            )
        ],
    )
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        NAVER_CLIENT_ID = Constants.NAVER_CLIENT_ID
        NAVER_CLIENT_SECRET = Constants.NAVER_CLIENT_SECRET
        NAVER_CALLBACK_URI = Constants.NAVER_CALLBACK_URI
        code = request.GET.get("code")
        state = "random_string"

        token_req = requests.post(
            f"https://nid.naver.com/oauth2.0/token?client_id={NAVER_CLIENT_ID}"
            f"&client_secret={NAVER_CLIENT_SECRET}&code={code}"
            f"&grant_type=authorization_code&redirect_uri={NAVER_CALLBACK_URI}"
            f"&state={state}"
        )
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get("error") == "invalid_request":
                return redirect(f"{BASE_URL}accounts/naver/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get("access_token")
        email_req = requests.get(f"https://openapi.naver.com/v1/nid/me?access_token={access_token}")
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return JsonResponse({"error": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST)
        email_req_json = email_req.json()
        email = email_req_json.get("response").get("email")
        if not email:
            return JsonResponse({"error": "email not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)

            if social_user.provider != "naver":
                return JsonResponse({"err_msg": "no matching social type"}, status=status.HTTP_400_BAD_REQUEST)
            data = {"access_token": access_token, "code": code}

            accept = requests.post(f"{BASE_URL}accounts/naver/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
            token = CustomJWTAuthentication.create_token(user)
            res = Response(data=token)
            return res

        except User.DoesNotExist:
            data = {"access_token": access_token, "code": code}
            accept = requests.post(f"{BASE_URL}accounts/naver/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
            user = User.objects.get(email=email)
            token = CustomJWTAuthentication.create_token(user)
            res = Response(data=token)
            return res


class NaverLoginToDjango(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = Constants.NAVER_CALLBACK_URI
    client_class = OAuth2Client
    schema = None


# ==================================================================== #
#                          카카오 소셜로그인                               #
# ==================================================================== #


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]
    schema = None

    def get(self, request):
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={Constants.REST_API_KEY}"
            f"&redirect_uri={Constants.KAKAO_CALLBACK_URI}&response_type=code"
        )


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="카카오 로그인 콜백",
        operation_description="카카오에서 반환한 인증 코드를 넣으면, 회원가입 or 로그인 후 서버 토큰 리턴\n"
        "닉네임이 없으면 message를 True 반환\n"
        "True면 닉네임, 프로필, 이름, 한줄 소개 업데이트",
        tags=["소셜 로그인"],
        manual_parameters=[
            openapi.Parameter(
                "code", in_=openapi.IN_QUERY, description="카카오에서 반환한 인증 코드", type=openapi.TYPE_STRING, required=True
            )
        ],
    )
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        REST_API_KEY = Constants.REST_API_KEY
        KAKAO_CALLBACK_URI = Constants.KAKAO_CALLBACK_URI
        code = request.GET.get("code")
        """
            Access Token Request
        """
        token_req = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}"
            f"&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
        )
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get("error") == "invalid_request":
                return redirect(f"{BASE_URL}accounts/kakao/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return JsonResponse({"err_msg": "email exists but not social user"}, status=status.HTTP_400_BAD_REQUEST)
            if social_user.provider != "kakao":
                return JsonResponse({"err_msg": "no matching social type"}, status=status.HTTP_400_BAD_REQUEST)
            data = {"access_token": access_token, "code": code}
            accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
            token = CustomJWTAuthentication.create_token(user)
            res = Response(data=token)
            return res
        except User.DoesNotExist:
            data = {"access_token": access_token, "code": code}
            accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({"err_msg": "failed to signup1"}, status=accept_status)
            user = User.objects.get(email=email)
            token = CustomJWTAuthentication.create_token(user)
            res = Response(data=token)
            return res


class KakaoLoginToDjango(SocialLoginView):
    permission_classes = [AllowAny]
    schema = None

    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = Constants.KAKAO_CALLBACK_URI

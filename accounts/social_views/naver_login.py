from allauth.socialaccount.providers.naver import views as naver_view

from accounts.views import *


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
                "code",
                in_=openapi.IN_QUERY,
                description="네이버에서 반환한 인증 코드",
                type=openapi.TYPE_STRING,
                required=True,
            ),
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
        email_req = requests.get(
            f"https://openapi.naver.com/v1/nid/me?access_token={access_token}"
        )
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return JsonResponse(
                {"error": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
            )
        email_req_json = email_req.json()
        email = email_req_json.get("response").get("email")
        if not email:
            return JsonResponse(
                {"error": "email not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)

            if social_user.provider != "naver":
                return JsonResponse(
                    {"err_msg": "no matching social type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {"access_token": access_token, "code": code}

            accept = requests.post(f"{BASE_URL}accounts/naver/login/finish/", data=data)
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
            accept = requests.post(f"{BASE_URL}accounts/naver/login/finish/", data=data)
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


class NaverLoginToDjango(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = Constants.NAVER_CALLBACK_URI
    client_class = OAuth2Client
    schema = None

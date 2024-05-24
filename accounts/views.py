from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, RegisterSerializer, TokenRefreshSerializer, UserSerializers
from core.exceptions.service_exceptions import *
from core.permissions import IsOwner
from core.responses import Response
from core.tokens import CustomJWTAuthentication


class RegisterView(APIView):
    """
    - 회원가입

    **Description**
    - 회원가입 시 사용하는 API입니다.
    """

    serializer_class = RegisterSerializer

    @swagger_auto_schema(operation_id="회원가입", tags=["사용자 인증"], request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise InvalidRequest

        serializer.save()

        return Response(data=serializer.data)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_id="로그인", tags=["사용자 인증"], request_body=LoginSerializer)
    def post(self, request):
        """
        - 로그인

        **Description**
        - 로그인 시 사용하는 API입니다.
        - 로그인 시 USERNAME_FIELD, PASSWORD를 입력받아 인증합니다.
        - 인증 완료 후 access-token과 refresh-token을 발행해줍니다.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise InvalidRequest

        return Response(data=serializer.data)


class TokenRefreshView(APIView):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(operation_id="토큰 재발급", tags=["사용자 인증"], request_body=TokenRefreshSerializer)
    def post(self, request):
        """
        - 토큰 재발급을 처리합니다.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise InvalidRequest

        return Response(data=serializer.data)


class UserInfoViews(APIView):
    permission_classes = [IsOwner]
    parser_classes = (MultiPartParser,)
    serializer_class = UserSerializers

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request, *args, **kwargs):
        """
        - 유저 정보 조회

        **Description**
        """
        user = CustomJWTAuthentication().authenticate(request)
        serializer = self.serializer_class(user[0])

        return Response(data=serializer.data)

    @swagger_auto_schema(tags=["유저 정보"], request_body=serializer_class)
    def patch(self, request, *args, **kwargs):
        """
        - 유저 정보 업데이트

        **Description**
        - Access Token을 이용하여 유저 정보를 업데이트 합니다
        """
        user = CustomJWTAuthentication().authenticate(request)
        serializer = self.serializer_class(user[0], data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(data=serializer.data)
        raise InvalidRequest

    def perform_update(self, serializer):
        user = CustomJWTAuthentication().authenticate(self.request)[0]
        if hasattr(user, "profile_img") and user.profile_img.path != "img/default/default_img.jpg":
            default_storage.delete(user.profile_img.path)
        serializer.save()

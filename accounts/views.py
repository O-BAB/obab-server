from django.core.files.storage import default_storage
from django.db import IntegrityError

from drf_yasg.utils import swagger_auto_schema

from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from accounts.serializers import (
    UserSerializers,
    RegisterSerializer,
    LoginSerializer,
    TokenRefreshSerializer,
)
from core.constants import SystemCodeManager
from core.responses import Response
from core.exceptions import raise_exception
from core.tokens import CustomJWTAuthentication
from core.responses import Response


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_id="회원가입",
        tags=["사용자 인증"],
        request_body=serializer_class,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise_exception(
                code=SystemCodeManager.get_message("base_code", "INVALID_FORMAT")
            )

        serializer.save()

        return Response(data=serializer.data)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id="로그인",
        tags=["사용자 인증"],
        request_body=LoginSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise_exception(
                code=SystemCodeManager.get_message("base_code", "INVALID_FORMAT")
            )

        return Response(data=serializer.data)


class TokenRefreshView(APIView):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        operation_id="토큰 재발급",
        tags=["사용자 인증"],
        request_body=TokenRefreshSerializer,
    )
    def post(self, request):
        """
        토큰 재발급을 처리합니다.
        """
        serializer = self.serializer_class(data=request.data)

        # Validation Check
        if not serializer.is_valid():
            raise_exception(
                code=SystemCodeManager.get_message("base_code", "INVALID_FORMAT")
            )

        return Response(data=serializer.data)


class UserInfoViews(APIView):
    parser_classes = (MultiPartParser,)
    serializer_class = UserSerializers

    def get_object(self):
        user = CustomJWTAuthentication().authenticate(self.request)
        return user

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request, *args, **kwargs):
        """
        유저 정보 조회
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(data=serializer.data)

    @swagger_auto_schema(tags=["유저 정보"])
    def patch(self, request, *args, **kwargs):
        """
        유저 정보 부분 수정
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(data=serializer.data)
        raise_exception(code=SystemCodeManager.get_message("base_code", "BAD_REQUEST"))

    def perform_update(self, serializer):
        instance = self.get_object()
        if (
            hasattr(instance, "profile_img")
            and instance.profile_img.path != "img/default/default_img.jpg"
        ):
            default_storage.delete(instance.profile_img.path)
        serializer.save()

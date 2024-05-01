from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from django.db import IntegrityError

from drf_yasg.utils import swagger_auto_schema

from rest_framework.parsers import MultiPartParser
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import request
from rest_framework import status

from accounts.serializers import UserSerializers, RegisterSerializer, LoginSerializer
from accounts.models import User
from core.tokens import TokenResponseSerializer
from core.tokens import get_user_id


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise ValidationError("올바른 포멧이 아닙니다.")

        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError(
                "이미 등록된 이메일 주소입니다.", code=status.HTTP_400_BAD_REQUEST
            )

        return Response(data=serializer.data)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                serializer = TokenResponseSerializer(user)
                return Response(data=serializer.to_representation(serializer))
            else:
                raise ValidationError(
                    "패스워드가 잘못되었습니다.", code=status.HTTP_400_BAD_REQUEST
                )

        except User.DoesNotExist:
            raise ValidationError(
                "가입되지 않은 사용자입니다.", code=status.HTTP_400_BAD_REQUEST
            )


class UserInfoViews(RetrieveUpdateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = UserSerializers
    http_method_names = ["get", "patch"]

    def get_object(self):
        user = get_user_id(self.request)
        return user

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request, *args, **kwargs):
        """
        유저 정보 조회
        ---
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["유저 정보"])
    def patch(self, request, *args, **kwargs):
        """
        유저 정보 부분 수정
        ---
        """
        return super().patch(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.profile_img.path != "img/default/default_img.jpg":
            default_storage.delete(instance.profile_img.path)
        serializer.save()

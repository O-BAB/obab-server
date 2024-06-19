from django.db import IntegrityError
from rest_framework import serializers

from accounts.models import User
from core.exceptions.service_exceptions import *
from core.tokens import CustomJWTAuthentication


class UserSerializers(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "email", "name", "nickname", "profile_img", "self_info", "created_at", "updated_at"]


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate_email(self, data):
        """
        Email 중복 검증
        """
        if User.objects.filter(email=data).exists():
            raise UserAlreadyExists
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise UnknownException

        return CustomJWTAuthentication.create_token(user)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user_info = UserSerializers(read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()

        if not user:
            raise UserNotFound

        if not user.check_password(password):
            raise UserPasswordInvalid

        if not user.is_active:
            raise UserIsNotAuthorized
        tokens = CustomJWTAuthentication.create_token(user)
        user_info = UserSerializers(user).data

        res = {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "user_info": user_info}

        print(res)

        return res


class TokenRefreshSerializer(serializers.Serializer):
    """
    토큰 재발급 시리얼 라이저
    """

    token = serializers.CharField(max_length=255, required=True, write_only=True, label="[Input]refresh_token")

    access_token = serializers.CharField(read_only=True, label="[Output]access_token")
    refresh_token = serializers.CharField(read_only=True, label="[Output]refresh_token")

    def validate(self, data):
        refresh_token = data.get("token")

        user = CustomJWTAuthentication().token_va(token=refresh_token)

        return CustomJWTAuthentication.create_token(user)

from django.db import IntegrityError

from rest_framework import serializers

from core.tokens import CustomJWTAuthentication
from core.constants import SystemCodeManager
from core.exceptions import raise_exception
from accounts.models import User


class UserSerializers(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "created_at",
            "updated_at",
            "email",
            "name",
            "nickname",
            "profile_img",
            "self_info",
        ]


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
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "EMAIL_ALREADY")
            )
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "USER_CREATE_ERROR")
            )

        return CustomJWTAuthentication.create_token(user)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()

        if not user:
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "USER_NOT_FOUND")
            )

        if not user.check_password(password):
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "USER_INVALID_PW")
            )

        if not user.is_active:
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "USER_NOT_ACTIVE")
            )

        return CustomJWTAuthentication.create_token(user)


class TokenRefreshSerializer(serializers.Serializer):
    """
    토큰 재발급 시리얼 라이저
    """

    token = serializers.CharField(
        max_length=255, required=True, write_only=True, label="[Input]refresh_token"
    )

    access_token = serializers.CharField(read_only=True, label="[Output]access_token")
    refresh_token = serializers.CharField(read_only=True, label="[Output]refresh_token")

    def validate(self, data):
        refresh_token = data.get("token")

        user = CustomJWTAuthentication().token_va(token=refresh_token)

        return CustomJWTAuthentication.create_token(user)

from rest_framework import serializers

from accounts.models import User
from core.exceptions.service_exceptions import UserAlreadyExists
from core.serializers import CustomTokenBlacklistSerializer, CustomTokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "nickname",
            "profile_img",
            "self_info",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "nickname", "password"]

    def is_valid(self, *, raise_exception=False):
        if User.objects.filter(email=self.initial_data.get("email")).exists():
            raise UserAlreadyExists
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return validated_data


class UserPatchSerializer(serializers.ModelSerializer):
    __options = {"required": False, "allow_null": True, "allow_blank": True}
    __image_options = {"required": False, "allow_null": True, "allow_empty_file": True}
    name = serializers.CharField(help_text="유저 이름", **__options)
    nickname = serializers.CharField(help_text="닉네임", **__options)
    profile_img = serializers.ImageField(help_text="프로필 이미지", **__image_options)
    self_info = serializers.CharField(help_text="한줄 소개", **__options)

    class Meta:
        model = User
        fields = ("name", "nickname", "profile_img", "self_info")


class UserLoginSerializer(CustomTokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD


class UserLogoutSerializer(CustomTokenBlacklistSerializer):
    """
    :comment: `access-token` used for get `refresh-token` from `refresh_jti`
               TokenBlacklistSerializer required `refresh-token` to move into blacklist-table.
    """

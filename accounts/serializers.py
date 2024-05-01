from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status

from accounts.models import User


class UserSerializers(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "created_at",
            "updated_at",
            "email",
            "name",
            "nickname",
            "profile_img",
            "self_info",
        ]


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255, required=True, write_only=True, label="[Input]이메일"
    )
    password = serializers.CharField(
        max_length=128, required=True, write_only=True, label="[Input]패스워드"
    )

    def validate(self, data):
        if User.objects.filter(email=data).exists():
            raise ValidationError(
                "이미 등록된 이메일 주소입니다.", code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        user = User.objects.create_user(email=email, password=password)

        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.constants import SystemCodeManager
from core.exceptions import raise_exception
from accounts.models import User


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "NOT_FOUND_TOKEN")
            )

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        return user, None

    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise_exception(
                    code=SystemCodeManager.get_message("auth_code", "USER_NOT_ACTIVE")
                )
            return user
        except User.DoesNotExist:
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "USER_NOT_FOUND")
            )

    @staticmethod
    def create_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }

    def token_va(self, token):
        try:
            refresh = RefreshToken(token)
            user_id = refresh["user_id"]
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise_exception(
                    code=SystemCodeManager.get_message("auth_code", "USER_NOT_ACTIVE")
                )
            return user
        except User.DoesNotExist:
            raise_exception(
                code=SystemCodeManager.get_message("auth_code", "USER_NOT_FOUND")
            )

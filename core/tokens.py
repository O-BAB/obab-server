from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from core.exceptions.service_exceptions import *


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raise InvalidRequest
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise JWTOutstandingNotFound

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        return user, None

    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise UserIsNotAuthorized
            return user
        except User.DoesNotExist:
            raise UserNotFound

    @staticmethod
    def create_token(user):
        refresh = RefreshToken.for_user(user)
        return {"refresh_token": str(refresh), "access_token": str(refresh.access_token)}

    def token_va(self, token):
        try:
            refresh = RefreshToken(token)
            user_id = refresh["user_id"]
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise UserIsNotAuthorized
            return user
        except User.DoesNotExist:
            raise UserNotFound

from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.exceptions import *
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from accounts.models import User
from core.exceptions.service_exceptions import UserIsNotAuthorized

from .mixins import TokenMixin


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, TokenMixin):
    def validate(self, attrs):
        if not self.is_active_user(_value=attrs.get(self.username_field), _value_type="email"):
            raise UserIsNotAuthorized

        _ = super(TokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        access = self.set_refresh_jti_into_access(refresh)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return {
            "id": self.user.id,
            "email": self.user.email,
            "nickname": self.user.nickname,
            "access_token": str(access),
            "refresh_token": str(refresh),
        }

    def get_token(self, user: User):
        """
        :comment: Get refresh token & check has already outstanding refresh-token.
        """
        refresh_token_instance = self.get_refresh_token_instance(filters={"user_id": user.id})
        if refresh_token_instance:
            """
            * If `refresh-token` is already outstanding, blacklisting it.
            * Only single device can access this app.
            """
            blacklist_serializer = TokenBlacklistSerializer(data={"refresh": refresh_token_instance.token})
            """
            * If `refresh-token` exist and not blacklisted but expired(or invalid),
              delete this token from database.
            """
            try:
                blacklist_serializer.is_valid()
            except (TokenError, TokenBackendError, InvalidToken, AuthenticationFailed):
                refresh_token_instance.delete()
        return super().get_token(user)


class CustomTokenBlacklistSerializer(TokenBlacklistSerializer, TokenMixin):
    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        return super().validate(attrs)

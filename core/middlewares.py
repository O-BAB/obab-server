from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from core.exceptions.service_exceptions import AccessTokenUnAuthorized, JWTOutstandingNotFound


class CustomJWTAuthentication(JWTAuthentication):
    """
    :comment: Validate access-token, refresh-token when client calling any APIs.
    """

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, AuthenticationFailed, TokenError):
            raise AccessTokenUnAuthorized

    def get_validated_token(self, raw_token):
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                # Verify access-token if refresh_jti matched with outstanding refresh-token and blacklisted.
                auth_token = AuthToken(raw_token)
                refresh_jti = auth_token.get("refresh_jti", "")
                refresh_token_instance = (
                    OutstandingToken.objects.filter(jti=refresh_jti)
                    .select_related("blacklistedtoken")
                    .filter(blacklistedtoken__isnull=True)
                    .first()
                )

                if not refresh_token_instance:
                    raise JWTOutstandingNotFound
                return auth_token
            except TokenError:
                raise AccessTokenUnAuthorized

        raise AccessTokenUnAuthorized

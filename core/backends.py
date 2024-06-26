from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import User
from core.exceptions.service_exceptions import AccessTokenUnAuthorized, UserNotFound, UserPasswordInvalid


class CustomJWTBackend(JWTAuthentication):
    """
    :comment: TokenObtainPairSerializer using this Authentication Class
    """

    def authenticate(self, request: Request, **credentials):
        """
        :param request: request object from `/admin/login` or `/api/v1/users/login`
        :param credentials: {"username": EMAIL_INFO, "password": "PASSWORD"} or
                            {"email": EMAIL_INFO, "password": "PASSWORD"}
        :return: user object.
        """
        _params = {
            self.user_model().USERNAME_FIELD: (
                credentials.get(self.user_model().USERNAME_FIELD) or credentials.get("username")
            )
        }
        user = User.objects.filter(**_params, is_active=True).first()

        if not user:
            raise UserNotFound
        if user and not user.check_password(credentials.get("password")):
            raise UserPasswordInvalid

        return user

    def get_user(self, _key):
        """
        :param _key: This value maybe `user id` or `JWT in dict`.

        :comment: if django admin session authentication, using `user id` to get user object.
                  if jwt(default) authentication, using `jwt` to get user object.
        """
        try:
            if isinstance(_key, int):
                #  if Django Admin Session, _key is `user's id`
                user_id = _key
                _filter = {"id": user_id}
            else:
                #  else API JWT
                _filter = {self.user_model().USERNAME_FIELD: _key[settings.SIMPLE_JWT_USER_ID_CLAIM]}
        except KeyError:
            raise AccessTokenUnAuthorized

        try:
            user = self.user_model.objects.get(**_filter)
        except self.user_model.DoesNotExist:
            raise UserNotFound
        except Exception:
            raise AccessTokenUnAuthorized

        if not user.is_active:
            raise AccessTokenUnAuthorized(message="서비스를 사용할 수 없는 유저입니다.")

        return user

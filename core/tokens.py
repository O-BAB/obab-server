from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from accounts.models import User

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class TokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = TokenObtainPairSerializer.get_token(user)
        self.user = user

    def get_access_token(self):
        return str(self.token.access_token)

    def get_refresh_token(self):
        return str(self.token)

    def to_representation(self, instance):
        nickname = self.user.nickname
        if nickname is None:
            message = True
        else:
            message = False

        return {
            "message": message,
            "token": {
                "email": self.user.email,
                "access": self.get_access_token(),
                "refresh": self.get_refresh_token(),
            },
        }


def get_user_id(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({'error': 'Authorization header is missing'}, status=400)

    try:
        access_token = auth_header.split(" ")[1]
        decoded = AccessToken(access_token)
        user_id = decoded["user_id"]
        user_instance = User.objects.get(id=user_id)
        return user_instance
    except AccessToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid access token'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
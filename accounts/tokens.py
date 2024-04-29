import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.views import TokenRefreshView
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

from rest_framework import permissions

from core.tokens import CustomJWTAuthentication
from core.exceptions.service_exceptions import *


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.user == CustomJWTAuthentication().authenticate(request)[0]:
            return True
        else:
            raise InvalidRequest


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        authenticated_user = CustomJWTAuthentication().authenticate(request)
        return obj.user == authenticated_user[0]


class UserPostAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomJWTAuthentication().authenticate(request)
        post_user = obj.foodrecipe.user

        if user == post_user:
            return True
        else:
            return False

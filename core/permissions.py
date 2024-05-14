from rest_framework import permissions

from core.tokens import CustomJWTAuthentication
from core.exceptions import raise_exception
from core.constants import SystemCodeManager

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.user == CustomJWTAuthentication().authenticate(request)[0]:
            return True
        else:
            raise_exception(code=SystemCodeManager.get_message("board_code","PermissionDenied"))


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

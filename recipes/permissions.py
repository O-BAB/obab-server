from rest_framework import permissions

from core.tokens import CustomJWTAuthentication


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == CustomJWTAuthentication.authenticate(request)


class UserPostAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomJWTAuthentication.authenticate(request)
        post_user = obj.foodrecipe.user

        if user == post_user:
            return True
        else:
            return False

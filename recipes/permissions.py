from rest_framework import permissions

from accounts.functions import get_user_id


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == get_user_id(request)


class UserPostAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = get_user_id(request)
        post_user = obj.foodrecipe.user

        if user == post_user:
            return True
        else:
            return False

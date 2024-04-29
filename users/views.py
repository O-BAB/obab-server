from drf_yasg.utils import swagger_auto_schema

from django.core.files.storage import default_storage

from rest_framework.parsers import MultiPartParser
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserSerializers
from accounts.functions import get_user_id


class UserInfoViews(RetrieveUpdateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = UserSerializers
    http_method_names = ["get", "patch"]

    def get_object(self):
        user = get_user_id(self.request)
        return user

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request, *args, **kwargs):
        """
        유저 정보 조회
        ---
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["유저 정보"])
    def patch(self, request, *args, **kwargs):
        """
        유저 정보 부분 수정
        ---
        """
        return super().patch(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.profile_img.path != "img/default/default_img.jpg":
            default_storage.delete(instance.profile_img.path)
        serializer.save()

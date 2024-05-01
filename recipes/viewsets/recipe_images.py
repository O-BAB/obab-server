from django.core.files.storage import default_storage

from drf_yasg.utils import swagger_auto_schema

from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication

from recipes.serializer import RecipeImageSerializer
from recipes.models import RecipeImage


class RecipeImageViewset(
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = RecipeImage.objects.all()
    serializer_class = RecipeImageSerializer
    authentication_classes = [JWTAuthentication]
    parser_classes = (MultiPartParser,)
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(state="임시저장")

    def perform_update(self, serializer):
        instance = self.get_object()
        default_storage.delete(instance.image.path)
        serializer.save(state="반영")

    def perform_destroy(self, instance):
        instance = self.get_object()
        default_storage.delete(instance.image.path)
        instance.delete()

    @swagger_auto_schema(tags=["레시피 이미지 업로드"])
    def create(self, request, *args, **kwargs):
        """
        레시피 이미지 생성
        ---
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 이미지 업로드"])
    def partial_update(self, request, *args, **kwargs):
        """
        레시피 이미지 전체 수정
        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 이미지 업로드"])
    def update(self, request, *args, **kwargs):
        """
        레시피 이미지 부분 수정
        ---
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 이미지 업로드"])
    def destroy(self, request, *args, **kwargs):
        """
        레시피 이미지 삭제
        ---
        """
        return super().destroy(request, *args, **kwargs)

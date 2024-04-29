from drf_yasg.utils import swagger_auto_schema

from recipes.serializer import RecipeImageSerializer
from recipes.models import RecipeImage
from core.viewsets import RecipeImageViewset


class RecipeImageViewset(RecipeImageViewset):
    queryset = RecipeImage.objects.all()
    serializer_class = RecipeImageSerializer

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

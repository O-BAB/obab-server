from drf_yasg.utils import swagger_auto_schema

from recipes.serializer import IngredientsSerializer
from recipes.models import Ingredients
from core.viewsets import BaseAbuotRecipesViewset


class IngredientsViewset(BaseAbuotRecipesViewset):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer

    @swagger_auto_schema(tags=["레시피 재료"])
    def create(self, request, *args, **kwargs):
        """
        레시피 재료 생성
        ---
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 재료"])
    def partial_update(self, request, *args, **kwargs):
        """
        레시피 재료 전체 수정
        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 재료"])
    def update(self, request, *args, **kwargs):
        """
        레시피 재료 부분 수정
        ---
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 재료"])
    def destroy(self, request, *args, **kwargs):
        """
        레시피 재료 삭제
        ---
        """
        return super().destroy(request, *args, **kwargs)

from drf_yasg.utils import swagger_auto_schema

from recipes.models import RecipeProcess
from core.viewsets import BaseAbuotRecipesViewset
from core.serializers import RecipeProcessSerializer


class RecipeProcessViewset(BaseAbuotRecipesViewset):
    queryset = RecipeProcess.objects.all()
    serializer_class = RecipeProcessSerializer

    @swagger_auto_schema(tags=["레시피 조리 과정"])
    def create(self, request, *args, **kwargs):
        """
        레시피 조리 과정 생성
        ---
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 조리 과정"])
    def partial_update(self, request, *args, **kwargs):
        """
        레시피 조리 과정 전체 수정
        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 조리 과정"])
    def update(self, request, *args, **kwargs):
        """
        레시피 조리 과정 부분 수정
        ---
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["레시피 조리 과정"])
    def destroy(self, request, *args, **kwargs):
        """
        레시피 조리 과정 삭제
        ---
        """
        return super().destroy(request, *args, **kwargs)

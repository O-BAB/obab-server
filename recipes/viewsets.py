from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from recipes.permissions import IsOwnerOrReadOnly
from core.tokens import CustomJWTAuthentication
from recipes.models import FoodRecipes
from recipes.serializer import FoodRecipesSerializer, ConvenienceRecipesDetailSerializer
from drf_yasg.utils import swagger_auto_schema

from core.responses import Response
from core.constants import SystemCodeManager
from core.exceptions import raise_exception


class RecipeDetail(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self, categoryCD):
        if categoryCD == "convenience_store_combination":
            return ConvenienceRecipesDetailSerializer
        return FoodRecipesSerializer

    def get_queryset(self, recipe_id):
        try:
            query = FoodRecipes.objects.get(id=recipe_id)
        except FoodRecipes.DoesNotExist:
            raise_exception(
                code=SystemCodeManager.get_message("board_code", "BOARD_INVALID")
            )

        return query

    @swagger_auto_schema(
        operation_id="레시피 상세 보기",
        tags=["레시피"],
    )
    def get(self, request, recipe_id):
        """
        레시피 상세 보기
        """
        queryset = self.get_queryset(recipe_id)
        serializer_class = self.get_serializer_class(queryset.categoryCD)
        serializer = serializer_class(queryset)

        return Response(data=serializer.data)

    @swagger_auto_schema(
        operation_id="레시피 수정",
        tags=["레시피"],
        request_body=ConvenienceRecipesDetailSerializer,
    )
    def patch(self, request, recipe_id):
        """
        레시피 수정
        """
        queryset = self.get_queryset(recipe_id)
        serializer_class = self.get_serializer_class(queryset.categoryCD)
        serializer = serializer_class(queryset, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save
        else:
            print("error")
        return Response(data=serializer.data)

    @swagger_auto_schema(
        operation_id="레시피 삭제",
        tags=["레시피"],
    )
    def delete(self, request, recipe_id):
        """
        레시피 삭제
        """
        print(recipe_id)
        recipe = FoodRecipes.objects.get(id=recipe_id)

        recipe.delete()

        return Response(data="성공적으로 삭제")

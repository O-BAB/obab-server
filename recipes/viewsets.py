from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.tokens import CustomJWTAuthentication
from core.constants import SystemCodeManager
from core.exceptions import raise_exception
from core.responses import Response

from recipes.permissions import IsOwnerOrReadOnly
from recipes.models import FoodRecipes
from recipes.serializer import (
    FoodRecipesDetailSerializer,
    ConvenienceRecipesDetailSerializer,
    ConvenienceRecipesListSerializer,
    FoodRecipesListSerializer,
    FoodrecipeSerializer,
)


class RecipeDetail(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self, categoryCD):
        if categoryCD == "convenience_store_combination":
            return ConvenienceRecipesDetailSerializer
        return FoodRecipesDetailSerializer

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
            raise_exception(
                code=SystemCodeManager.get_message("board_code", "BOARD_INVALID")
            )
        return Response(data=serializer.data)

    @swagger_auto_schema(
        operation_id="레시피 삭제",
        tags=["레시피"],
    )
    def delete(self, request, recipe_id):
        """
        레시피 삭제
        """
        recipe = FoodRecipes.objects.get(id=recipe_id)

        recipe.delete()

        return Response(data="성공적으로 삭제")


class RecipeListView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self, categoryCD):
        if categoryCD == "convenience_store_combination":
            return ConvenienceRecipesListSerializer
        return FoodRecipesListSerializer

    def get_queryset(self, category_cd):
        return FoodRecipes.objects.filter(categoryCD=category_cd)

    @swagger_auto_schema(
        operation_id="레시피 목록",
        tags=["레시피"],
        manual_parameters=[
            openapi.Parameter(
                "categoryCD",
                in_=openapi.IN_QUERY,
                description="카테고리를 선택하세요.",
                type=openapi.TYPE_STRING,
                enum=[
                    "food_recipe",
                    "broadcast_recipe",
                    "convenience_store_combination",
                    "seasoning_recipe",
                    "cooking_tip",
                ],
                required=True,
            ),
        ],
    )
    def get(self, request):
        """
        카테고리별 목록 보기
        """
        category_cd = request.GET.get("categoryCD")
        queryset = self.get_queryset(category_cd)
        serializer_class = self.get_serializer_class(category_cd)
        serializer = serializer_class(queryset, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(
        operation_id="레시피 생성",
        tags=["레시피"],
        request_body=FoodrecipeSerializer,
    )
    def post(self, request):
        """
        레시피 생성
        """
        serializer = FoodrecipeSerializer(data=request.data)
        user = CustomJWTAuthentication().authenticate(self.request)
        if serializer.is_valid():
            serializer.save(user=user[0])
            return Response(data=serializer.data)
        else:
            raise_exception(
                code=SystemCodeManager.get_message("board_code", "BOARD_INVALID")
            )

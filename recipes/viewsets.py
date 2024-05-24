from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from core.exceptions.service_exceptions import *
from core.paginations import CustomPagination
from core.permissions import IsOwnerOrReadOnly
from core.responses import Response
from core.tokens import CustomJWTAuthentication
from recipes.models import FoodRecipes
from recipes.serializers import (
    ConvenienceCreateUpdateSerializer,
    ConvenienceRecipesListSerializer,
    FoodRecipesListSerializer,
    ImageUploadSerializer,
    basicCreateUpdateSerializer,
)


class basicCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(operation_id="일반 레시피 생성", tags=["레시피"], request_body=basicCreateUpdateSerializer)
    def post(self, request):
        """
        - 일반 레시피 생성

        **Description**
        카테고리 목록
        - food_recipe, 음식 레시피
        - broadcast_recipe, 방송 레시피
        - seasoning_recipe, 양념 레시피
        - cooking_tip, 요리 TIP
        """
        serializer = basicCreateUpdateSerializer(data=request.data)
        user = CustomJWTAuthentication().authenticate(self.request)

        if serializer.is_valid():
            serializer.save(user=user[0])
            return Response(data=serializer.data)
        else:
            raise InvalidRequest


class basicUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(operation_id="일반 레시피 수정", tags=["레시피"], request_body=basicCreateUpdateSerializer)
    def put(self, request, *args, **kwargs):
        """
        - 일반 레시피 수정

        **Description**
        카테고리 목록
        - food_recipe, 음식 레시피
        - broadcast_recipe, 방송 레시피
        - seasoning_recipe, 양념 레시피
        - cooking_tip, 요리 TIP
        """
        recipe_id = kwargs.get("id")
        try:
            recipe = FoodRecipes.objects.get(pk=recipe_id)
            self.check_object_permissions(self.request, recipe)
        except FoodRecipes.DoesNotExist:
            raise RecipeNotFound
        serializer = basicCreateUpdateSerializer(recipe, data=request.data)
        user = CustomJWTAuthentication().authenticate(request)
        if serializer.is_valid():
            serializer.save(user=user[0])
            return Response(data=serializer.data)
        else:
            raise InvalidRequest


class convenienceCreateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(operation_id="편의점 레시피 생성", tags=["레시피"], request_body=ConvenienceCreateUpdateSerializer)
    def post(self, request):
        """
        - 편의점 레시피 생성

        **Description**
        - 카테고리는 "convenience_store_combination" 로 해주세요.
        """
        serializer = ConvenienceCreateUpdateSerializer(data=request.data)
        user = CustomJWTAuthentication().authenticate(request)

        if serializer.is_valid():
            serializer.save(user=user[0])
            return Response(data=serializer.data)
        else:
            raise InvalidRequest


class convenienceUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(operation_id="편의점 레시피 수정", tags=["레시피"], request_body=ConvenienceCreateUpdateSerializer)
    def put(self, request, *args, **kwargs):
        """
        - 편의점 레시피 수정

        **Description**
        - 카테고리는 "convenience_store_combination" 로 해주세요.
        """
        recipe_id = kwargs.get("id")
        try:
            recipe = FoodRecipes.objects.get(pk=recipe_id)
            self.check_object_permissions(self.request, recipe)
        except FoodRecipes.DoesNotExist:
            raise RecipeNotFound
        serializer = ConvenienceCreateUpdateSerializer(recipe, data=request.data)
        user = CustomJWTAuthentication().authenticate(request)

        if serializer.is_valid():
            serializer.save(user=user[0])
            return Response(data=serializer.data)
        else:
            raise InvalidRequest


class RecipeViewset(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPagination
    swagger_fake_view = False

    def get_serializer_class(self, categoryCD=None):
        if getattr(self, "swagger_fake_view", False) or categoryCD is None:
            return FoodRecipesListSerializer
        if categoryCD == "convenience_store_combination":
            return ConvenienceRecipesListSerializer
        return FoodRecipesListSerializer

    def get_queryset(self, category_cd=None):
        if getattr(self, "swagger_fake_view", False) or category_cd is None:
            return FoodRecipes.objects.none()
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
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        """
        - 카테고리별 목록 보기

        **Description**
        - 카테고리를 선택하면 관련된 게시물 목록을 보여줍니다.
        - page_size는 몇개씩 보여줄 것인지 입니다.
        - page는 몇번째 페이지를 로드할지 입니다.
        """
        category_cd = request.GET.get("categoryCD")
        queryset = self.get_queryset(category_cd)
        serializer_class = self.get_serializer_class(category_cd)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(operation_id="레시피 상세 보기", tags=["레시피"])
    def retrieve(self, request, *args, **kwargs):
        """
        - 레시피 상세 조회

        **Description**
        - 게시물 ID를 입력하면 게시물을 상세 조회합니다.
        """
        recipe_id = kwargs.get("pk")
        try:
            queryset = FoodRecipes.objects.get(id=recipe_id)
        except FoodRecipes.DoesNotExist:
            raise RecipeNotFound
        if queryset.categoryCD == "convenience_store_combination":
            serializer_class = ConvenienceCreateUpdateSerializer
        else:
            serializer_class = basicCreateUpdateSerializer
        serializer = serializer_class(queryset)
        return Response(data=serializer.data)

    @swagger_auto_schema(operation_id="레시피 삭제", tags=["레시피"])
    def destroy(self, request, *args, **kwargs):
        """
        - 레시피 삭제

        **Description**
        - 게시물 ID를 입력하면 게시물을 삭제합니다.
        """
        recipe_id = kwargs.get("pk")
        recipe = FoodRecipes.objects.get(id=recipe_id)
        self.check_object_permissions(self.request, recipe)
        recipe.delete()

        return Response(data="성공적으로 삭제")


class ImageUploadView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    parser_classes = (MultiPartParser,)
    permission_classes = []

    @swagger_auto_schema(tags=["레시피 이미지 업로드"], request_body=ImageUploadSerializer)
    def post(self, request):
        """
        - 이미지 업로드

        **Description**
        - 이미지 파일을 업로드 해주면 저장된 경로를 리턴해줍니다.
        """
        serializer = ImageUploadSerializer(data=request.data)
        user = CustomJWTAuthentication().authenticate(self.request)[0]

        if serializer.is_valid():
            serializer.save(user=user, state="임시저장")
            return Response(data=serializer.data)
        else:
            raise InvalidRequest

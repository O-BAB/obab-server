from django.core.files.storage import default_storage

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from core.tokens import CustomJWTAuthentication
from core.paginations import CustomPagination
from core.exceptions.service_exceptions import *
from core.responses import Response

from core.permissions import IsOwnerOrReadOnly
from recipes.models import FoodRecipes
from recipes.serializers import (
    basicCreateUpdateSerializer,
    ConvenienceCreateUpdateSerializer,
    ConvenienceRecipesListSerializer,
    FoodRecipesListSerializer,
    ImageUploadSerializer,
)


class basicCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_id="일반 레시피 생성",
        tags=["레시피"],
        request_body=basicCreateUpdateSerializer,
    )
    def post(self, request):
        """
        일반 레시피 생성
        ---
        food_recipe, 음식 레시피
        broadcast_recipe, 방송 레시피
        seasoning_recipe, 양념 레시피
        cooking_tip, 요리 TIP
        """
        serializer = basicCreateUpdateSerializer(data=request.data)
        user = CustomJWTAuthentication().authenticate(self.request)

        if not serializer.is_valid():
            print(serializer.errors)

        if serializer.is_valid():
            serializer.save(user=user[0])
            return Response(data=serializer.data)
        else:
            raise InvalidRequest


class basicUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_id="일반 레시피 수정",
        tags=["레시피"],
        request_body=basicCreateUpdateSerializer,
    )
    def put(self, request, *args, **kwargs):
        """
        일반 레시피 수정
        ---
        food_recipe, 음식 레시피
        broadcast_recipe, 방송 레시피
        seasoning_recipe, 양념 레시피
        cooking_tip, 요리 TIP
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

    @swagger_auto_schema(
        operation_id="편의점 레시피 생성",
        tags=["레시피"],
        request_body=ConvenienceCreateUpdateSerializer,
    )
    def post(self, request):
        """
        편의점 레시피 생성
        ---
        convenience_store_combination, 편의점 꿀 조합
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

    @swagger_auto_schema(
        operation_id="편의점 레시피 수정",
        tags=["레시피"],
        request_body=ConvenienceCreateUpdateSerializer,
    )
    def put(self, request, *args, **kwargs):
        """
        편의점 레시피 수정
        ---
        convenience_store_combination, 편의점 꿀 조합
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
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
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
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """
        카테고리별 목록 보기
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

    @swagger_auto_schema(
        operation_id="레시피 상세 보기",
        tags=["레시피"],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        레시피를 상세 조회
        """
        recipe_id = kwargs.get("pk")
        try:
            queryset = FoodRecipes.objects.get(id=recipe_id)
        except:
            raise RecipeNotFound
        if queryset.categoryCD == "convenience_store_combination":
            serializer_class = ConvenienceCreateUpdateSerializer
        else:
            serializer_class = basicCreateUpdateSerializer
        serializer = serializer_class(queryset)
        return Response(data=serializer.data)

    @swagger_auto_schema(
        operation_id="레시피 삭제",
        tags=["레시피"],
    )
    def destroy(self, request, *args, **kwargs):
        """
        레시피 삭제
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

    @swagger_auto_schema(
        tags=["레시피 이미지 업로드"],
        request_body=ImageUploadSerializer,
    )
    def post(self, request):
        """
        레시피 이미지 생성
        ---
        """
        serializer = ImageUploadSerializer(data=request.data)
        user = CustomJWTAuthentication().authenticate(self.request)[0]

        if serializer.is_valid():
            serializer.save(user=user, state="임시저장")
            return Response(data=serializer.data)
        else:
            raise InvalidRequest

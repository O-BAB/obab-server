from rest_framework.viewsets import GenericViewSet

from core.exceptions.service_exceptions import InvalidRequest, RecipeNotFound
from core.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    MappingViewSetMixin,
    RetrieveModelMixin,
    SimpleJWTMixin,
    UpdateModelMixin,
)
from recipes.models import FoodRecipes
from recipes.serializers import BasicRecipeSerializer, ConvenienceRecipeSerializers, FoodRecipesSerializer


class FoodrecipeViewsets(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    MappingViewSetMixin,
    SimpleJWTMixin,
    GenericViewSet,
):
    serializer_action_map = {
        "create_basic": BasicRecipeSerializer,
        "create_convenience": ConvenienceRecipeSerializers,
        "partial_basic": BasicRecipeSerializer,
        "partial_convenience": ConvenienceRecipeSerializers,
        "retrieve": BasicRecipeSerializer,
        "list": FoodRecipesSerializer,
    }
    queryset = FoodRecipes.objects.all()

    def create_basic(self, request, *args, **kwargs):
        """
        - 일반 레시피 생성

        **Description**
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        - 레시피 상세 조회

        **Description**
        - ID를 입력해주세요.
        """
        try:
            instance = self.get_object()
            if instance.categoryCD == "convenience":
                self.serializer_class = ConvenienceRecipeSerializers
            return super().retrieve(request, *args, **kwargs)
        except self.queryset.model.DoesNotExist:
            raise RecipeNotFound

    def partial_basic(self, request, *args, **kwargs):
        """
        - 일반 레시피 수정

        **Description**
        - 수정할 값만 입력해주시면 됩니다.
        - recipeProcess.id, recipeIngredients.id는 필수로 입력해주세요
        """
        try:
            instance = self.get_object()
            if instance.user != request.user:
                raise InvalidRequest
            return super().partial_update(request, *args, **kwargs)
        except self.queryset.model.DoesNotExist:
            raise RecipeNotFound

    def list(self, request, *args, **kwargs):
        """
        - 레시피 목록

        **Description**
        - 파라미터로 category를 보내면 카테고리별 리스트
        """
        category = self.kwargs.get("category")
        if category:
            self.queryset = FoodRecipes.objects.filter(categoryCD=category)
        else:
            self.queryset = FoodRecipes.objects.all()
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        - 레시피 삭제

        **Description**
        - ID를 입력해주세요.
        """
        try:
            instance = self.get_object()
            if instance.user != request.user:
                raise InvalidRequest
            return super().destroy(request, *args, **kwargs)
        except self.queryset.model.DoesNotExist:
            raise RecipeNotFound

    def create_convenience(self, request, *args, **kwargs):
        """
        - 편의점 레시피 생성

        **Description**
        """
        return super().create(request, *args, **kwargs)

    def partial_convenience(self, request, *args, **kwargs):
        """
        - 편의점 레시피 수정

        **Description**
        - 수정할 값만 입력해주시면 됩니다.
        - convenienceItems.id, recipeIngredients.id는 필수로 입력해주세요
        """
        try:
            instance = self.get_object()
            if instance.user != request.user:
                raise InvalidRequest
            return super().partial_update(request, *args, **kwargs)
        except self.queryset.model.DoesNotExist:
            raise RecipeNotFound

    def get_object(self):
        try:
            return super().get_object()
        except self.queryset.model.DoesNotExist:
            return RecipeNotFound

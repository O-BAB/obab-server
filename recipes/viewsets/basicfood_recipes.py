from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from recipes.permissions import IsOwnerOrReadOnly

from core.tokens import CustomJWTAuthentication
from recipes.models import FoodRecipes
from recipes.serializer import FoodRecipesSerializer


# FoodRecipes
class FoodRecipesViewSet(viewsets.ModelViewSet):
    categoryCD = "food_recipe"
    queryset = FoodRecipes.objects.filter(categoryCD=categoryCD)
    serializer_class = FoodRecipesSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            categoryCD=self.categoryCD,
            user=CustomJWTAuthentication().authenticate(self.request),
        )

    @swagger_auto_schema(tags=["일반 음식 레시피"])
    def list(self, request, *args, **kwargs):
        """
        일반 음식 레시피 목록
        ---
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["일반 음식 레시피"])
    def create(self, request, *args, **kwargs):
        """
        일반 음식 레시피 생성
        ---
        thumnail : 썸네일 이미지
        tot_price : 전체 가격
        intro : 한줄 소개
        time : 시간 (ex. 03:30)
        video : 참고 동영상 url
        people_num : 인분
        difficulty : 난이도
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["일반 음식 레시피"])
    def retrieve(self, request, *args, **kwargs):
        """
        일반 음식 레시피 상세 읽기
        ---
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["일반 음식 레시피"])
    def update(self, request, *args, **kwargs):
        """
        일반 음식 레시피 전체 수정
        ---
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["일반 음식 레시피"])
    def partial_update(self, request, *args, **kwargs):
        """
        일반 음식 레시피 부분 수정
        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["일반 음식 레시피"])
    def destroy(self, request, *args, **kwargs):
        """
        일반 음식 레시피 삭제
        ---
        """
        return super().destroy(request, *args, **kwargs)

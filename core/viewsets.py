from django.core.files.storage import default_storage

from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from recipes.permissions import IsOwnerOrReadOnly, UserPostAccessPermission
from accounts.functions import get_user_id
from recipes.models import FoodRecipes


class BaseRecipesViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=get_user_id(self.request))

    @swagger_auto_schema(tags=["카테고리 별 게시물 목록"])
    def list(self, request, *args, **kwargs):
        """
        카테고리 별 게시물 목록
        ---
        food_recipe : 일반 음식 레시피
        broadcast_recipe : 방송에서 핫한 레시피
        seasoning_recipe : 양념 레시피
        convenience_store_combination : 편의점 레시피
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["카테고리 별 게시물 생성"])
    def create(self, request, *args, **kwargs):
        """
        게시물 생성
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

    @swagger_auto_schema(tags=["카테고리 별 게시물 읽기"])
    def retrieve(self, request, *args, **kwargs):
        """
        세부 내용 읽기
        ---
        모든 게시물은 하나의 테이블로 이루어져 있어, 카테고리 별 알맞은 id를 입력해야합니다.
        예시) id가 1이고 카테고리가 food_recipe인 게시물을 참고 할때는 food_recipe의 url로 id값을 보내야합니다.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["카테고리 별 게시물 전체 수정"])
    def update(self, request, *args, **kwargs):
        """
        전체 수정
        ---
        모든 게시물은 하나의 테이블로 이루어져 있어, 카테고리 별 알맞은 id를 입력해야합니다.
        예시) id가 1이고 카테고리가 food_recipe인 게시물을 참고 할때는 food_recipe의 url로 id값을 보내야합니다.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["카테고리 별 게시물 부분 수정"])
    def partial_update(self, request, *args, **kwargs):
        """
        부분 수정
        ---
        모든 게시물은 하나의 테이블로 이루어져 있어, 카테고리 별 알맞은 id를 입력해야합니다.
        예시) id가 1이고 카테고리가 food_recipe인 게시물을 참고 할때는 food_recipe의 url로 id값을 보내야합니다.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["카테고리 별 게시물 삭제"])
    def destroy(self, request, *args, **kwargs):
        """
        삭제
        ---
        모든 게시물은 하나의 테이블로 이루어져 있어, 카테고리 별 알맞은 id를 입력해야합니다.
        예시) id가 1이고 카테고리가 food_recipe인 게시물을 참고 할때는 food_recipe의 url로 id값을 보내야합니다.
        """
        return super().destroy(request, *args, **kwargs)


class BaseAbuotRecipesViewset(
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    parser_classes = (MultiPartParser,)
    authentication_classes = [JWTAuthentication]
    permission_classes = [UserPostAccessPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_id(self.request)
        instance = serializer.validated_data["foodrecipe"]
        post_id = instance.id
        post_user = FoodRecipes.objects.get(id=post_id).user

        if user != post_user:
            return Response(
                {"error": "자격 인증 데이터가 잘못되었습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.create_response(serializer, instance)

    def create_response(self, serializer, instance):
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class RecipeImageViewset(
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    parser_classes = (MultiPartParser,)
    authentication_classes = [JWTAuthentication]
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

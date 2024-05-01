from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import FoodRecipes
from core.tokens import get_user_id


class LikeToggleAPIView(APIView):
    @swagger_auto_schema(
        operation_id="게시물 좋아요",
        tags=["좋아요&북마크"],
        manual_parameters=[
            openapi.Parameter(
                "id",
                in_=openapi.IN_QUERY,
                description="게시물 id",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def post(self, request):
        recipe_id = request.GET.get("id")
        recipe = get_object_or_404(FoodRecipes, id=recipe_id)
        user = get_user_id(self.request)

        if user in recipe.like.all():
            recipe.like.remove(user)
            liked = False
        else:
            recipe.like.add(user)
            liked = True

        return Response({"liked": liked}, status=status.HTTP_200_OK)


class BookmarkToggleAPIView(APIView):
    @swagger_auto_schema(
        operation_id="게시물 북마크",
        tags=["좋아요&북마크"],
        manual_parameters=[
            openapi.Parameter(
                "id",
                in_=openapi.IN_QUERY,
                description="게시물 id",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    def post(self, request):
        recipe_id = request.GET.get("id")
        recipe = get_object_or_404(FoodRecipes, id=recipe_id)
        user = get_user_id(self.request)

        if user in recipe.bookmark.all():
            recipe.bookmark.remove(user)
            bookmarked = False
        else:
            recipe.bookmark.add(user)
            bookmarked = True

        return Response({"bookmarked": bookmarked}, status=status.HTTP_200_OK)


from django.db.models import Count

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from recipes.models import FoodRecipes, Ingredients
from recipes.serializer import SearchRecipeSerializer


class SearchRecipe(APIView):
    @swagger_auto_schema(
        operation_id="검색 기능",
        operation_description="레시피를 검색하고 필터링합니다.",
        tags=["검색"],
        manual_parameters=[
            openapi.Parameter(
                "title",
                in_=openapi.IN_QUERY,
                description="검색어를 입력하세요.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
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
                required=False,
            ),
            openapi.Parameter(
                "ingredients",
                in_=openapi.IN_QUERY,
                description="재료를 입력하세요.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "sort_by",
                in_=openapi.IN_QUERY,
                description="정렬 기준을 선택하세요.",
                enum=["latest", "like", "bookmark"],
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
    )
    def get(self, request):
        title = request.query_params.get("title", "")
        category = request.query_params.get("categoryCD", "")
        ingredients = request.query_params.get("ingredients", "")
        sort_by = request.query_params.get("sort_by", "")

        queryset = FoodRecipes.objects.all()

        if category:
            queryset = queryset.filter(categoryCD__icontains=category)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if ingredients:
            ingredient = Ingredients.objects.filter(name__icontains=ingredients)
            queryset = queryset.filter(id__in=[ing.foodrecipe_id for ing in ingredient])

        if sort_by == "latest":
            queryset = queryset.order_by("-created_at")
        elif sort_by == "like":
            queryset = queryset.annotate(like_count=Count("like"))
            queryset = queryset.order_by("-like_count")
        elif sort_by == "bookmark":
            queryset = queryset.annotate(bookmark_count=Count("bookmark"))
            queryset = queryset.order_by("-bookmark_count")

        serializer = SearchRecipeSerializer(queryset, many=True)

        return Response(serializer.data)

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
        recipe_id = request.GET.get('id')
        recipe = get_object_or_404(FoodRecipes, id=recipe_id)
        user = get_user_id(self.request)
        
        if user in recipe.like.all():
            recipe.like.remove(user)
            liked = False
        else:
            recipe.like.add(user)
            liked = True
        
        return Response({'liked': liked}, status=status.HTTP_200_OK)


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
        recipe_id = request.GET.get('id')
        recipe = get_object_or_404(FoodRecipes, id=recipe_id)
        user = get_user_id(self.request)
        
        if user in recipe.bookmark.all():
            recipe.bookmark.remove(user)
            bookmarked = False
        else:
            recipe.bookmark.add(user)
            bookmarked = True
        
        return Response({'bookmarked': bookmarked}, status=status.HTTP_200_OK)

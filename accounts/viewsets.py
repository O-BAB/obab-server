from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from core.permissions import IsOwnerOrReadOnly
from core.tokens import CustomJWTAuthentication
from core.paginations import CustomPagination
from core.responses import Response

from recipes.serializers import FoodRecipesListSerializer
from recipes.models import FoodRecipes
from comments.models import Comments
from comments.serializers import CommentSerializer


class RecipeBookmarkList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FoodRecipesListSerializer
    pagination_class = CustomPagination()

    def get_queryset(self):
        user = CustomJWTAuthentication().authenticate(self.request)
        return FoodRecipes.objects.filter(bookmark=user[0])

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request):
        """
        북마크 목록
        """
        self.queryset = self.get_queryset()
        page = self.pagination_class.paginate_queryset(
            self.queryset, request, view=self
        )
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)
        else:
            return Response(data=serializer.data)


class RecipeWriteList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FoodRecipesListSerializer
    pagination_class = CustomPagination()

    def get_queryset(self):
        user = CustomJWTAuthentication().authenticate(self.request)
        return FoodRecipes.objects.filter(user=user[0])

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request, *args, **kwargs):
        """
        작성글 목록
        """
        self.queryset = self.get_queryset()
        page = self.pagination_class.paginate_queryset(
            self.queryset, request, view=self
        )
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)
        else:
            return Response(data=serializer.data)


class RecipeCommentList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = CustomPagination()

    def get_queryset(self):
        user = CustomJWTAuthentication().authenticate(self.request)
        return Comments.objects.filter(user=user[0])

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request, *args, **kwargs):
        """
        작성한 댓글 목록
        """
        self.queryset = self.get_queryset()
        page = self.pagination_class.paginate_queryset(
            self.queryset, request, view=self
        )
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            for item in serializer.data:
                recipe_id = item["recipe"]
                item["title"] = FoodRecipes.objects.get(id=recipe_id).title
            return self.pagination_class.get_paginated_response(serializer.data)
        else:
            return Response(data=serializer.data)

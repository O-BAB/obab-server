from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from core.permissions import IsOwnerOrReadOnly
from core.tokens import CustomJWTAuthentication
from core.responses import Response

from recipes.serializers import FoodRecipesListSerializer
from recipes.models import FoodRecipes


class RecipeBookmarkList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FoodRecipesListSerializer

    def get_queryset(self):
        user = CustomJWTAuthentication().authenticate(self.request)
        return FoodRecipes.objects.filter(bookmark=user[0])

    @swagger_auto_schema(tags=["유저 정보"])
    def get(self, request):
        """
        북마크 목록
        """
        self.queryset = self.get_queryset()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data)

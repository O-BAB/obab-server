from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication

from recipes.serializer import ConvenienceItemsSerializer
from recipes.permissions import UserPostAccessPermission
from recipes.models import ConvenienceItems
from core.tokens import CustomJWTAuthentication
from recipes.models import FoodRecipes


class ConvenienceItemsViewset(viewsets.ModelViewSet):
    queryset = ConvenienceItems.objects.all()
    serializer_class = ConvenienceItemsSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = [JWTAuthentication]
    permission_classes = [UserPostAccessPermission]

    @swagger_auto_schema(tags=["편의점 꿀 조합 재료"])
    def create(self, request, *args, **kwargs):
        """
        편의점 재료 생성
        ---
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomJWTAuthentication().authenticate(self.request)
        instance = serializer.validated_data["foodrecipe"]
        post_id = instance.id
        post_user = FoodRecipes.objects.get(id=post_id).user

        if user != post_user:
            return Response(
                {"error": "자격 인증 데이터가 잘못되었습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["편의점 꿀 조합 재료"])
    def partial_update(self, request, *args, **kwargs):
        """
        편의점 재료 부분 수정
        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["편의점 꿀 조합 재료"])
    def update(self, request, *args, **kwargs):
        """
        편의점 재료 전체 수정
        ---
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["편의점 꿀 조합 재료"])
    def destroy(self, request, *args, **kwargs):
        """
        편의점 재료 삭제
        ---
        """
        instance = self.get_object()
        price = instance.price
        foodrecipe = instance.foodrecipe
        tot_price = foodrecipe.tot_price - price

        foodrecipe.tot_price = tot_price
        foodrecipe.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create_response(self, serializer, instance):
        response = super().create_response(serializer, instance)
        price = serializer.data["price"]
        instance.tot_price += price
        instance.save()
        return response

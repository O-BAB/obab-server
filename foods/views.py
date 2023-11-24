from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Food
from .serializers import FoodSearchSerializer


class SearchFood(ListAPIView):
    serializer_class = FoodSearchSerializer

    def generate_condition(self, field_name, value):
        condition = (
            ~Q(**{f"{field_name}__icontains": "all"})
            if value == "all"
            else Q(**{f"{field_name}__icontains": value})
        )
        return condition

    def post(self, request):
        food_type = request.data.get("food_type")
        weight = request.data.get("weight")
        temperature = request.data.get("temperature")
        spicy_level = request.data.get("spicy_level")
        meat_type = request.data.get("meat_type")
        cooking_method = request.data.get("cooking_method")

        food_type_condition = self.generate_condition("food_type", food_type)
        weight_condition = self.generate_condition("weight", weight)
        temperature_condition = self.generate_condition("temperature", temperature)
        spicy_level_condition = self.generate_condition("spicy_level", spicy_level)
        meat_type_condition = self.generate_condition("meat_type", meat_type)
        cooking_method_condition = self.generate_condition(
            "cooking_method", cooking_method
        )

        queryset = Food.objects.filter(
            food_type_condition
            & weight_condition
            & temperature_condition
            & spicy_level_condition
            & meat_type_condition
            & cooking_method_condition
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

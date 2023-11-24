from rest_framework import serializers
from .models import Food


class FoodSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        exclude = ["is_activate", "suggestion_user"]

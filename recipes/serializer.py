from rest_framework import serializers

from core.serializers import BaseRecipeSerializer
from recipes.models import FoodRecipes, Ingredients, ConvenienceItems, RecipeImage


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = "__all__"


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = "__all__"


class ConvenienceItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvenienceItems
        fields = "__all__"


class FoodRecipesSerializer(BaseRecipeSerializer):
    ingredients = serializers.SerializerMethodField()
    categoryCD = serializers.ReadOnlyField()

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "user",
            "profile",
            "title",
            "thumnail",
            "categoryCD",
            "intro",
            "time",
            "video",
            "people_num",
            "difficulty",
            "created_at",
            "updated_at",
            "ingredients",
            "recipeprocess",
            "comments",
        ]

    def get_ingredients(self, data):
        ingredient = Ingredients.objects.filter(foodrecipe=data.id)
        serializer = IngredientsSerializer(ingredient, many=True)
        return serializer.data


class ConvenienceRecipesSerializer(BaseRecipeSerializer):
    convenience_item = serializers.SerializerMethodField()
    categoryCD = serializers.ReadOnlyField()

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "user",
            "profile",
            "title",
            "thumnail",
            "categoryCD",
            "tot_price",
            "intro",
            "time",
            "video",
            "difficulty",
            "created_at",
            "updated_at",
            "convenience_item",
            "recipeprocess",
            "comments",
        ]

    def get_convenience_item(self, data):
        convenience_item = ConvenienceItems.objects.filter(foodrecipe=data.id)
        serializer = ConvenienceItemsSerializer(convenience_item, many=True)
        return serializer.data


class SearchRecipeSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "like_count",
            "bookmark_count",
            "created_at",
            "updated_at",
            "categoryCD",
            "title",
            "tot_price",
            "thumnail",
            "video",
            "intro",
            "time",
            "people_num",
            "difficulty",
            "user",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()

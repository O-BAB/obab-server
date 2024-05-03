from rest_framework import serializers

from recipes.models import FoodRecipes, Ingredients, ConvenienceItems, RecipeImage
from recipes.models import RecipeProcess
from comments.serializers import CommentSerializer


class RecipeProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeProcess
        fields = "__all__"


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


class FoodrecipeSerializer(serializers.ModelSerializer):
    tot_price = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()

    class Meta:
        model = FoodRecipes
        fields = "__all__"


class FoodRecipesDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    thumnail_url = serializers.ImageField(source="thumnail", use_url=True)
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    recipe_ingredients = IngredientsSerializer(many=True, read_only=True)
    recipe_process = RecipeProcessSerializer(many=True, read_only=True)
    recipe_image = RecipeImageSerializer(many=True, read_only=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "categoryCD",
            "user",
            "title",
            "recipe_ingredients",
            "thumnail_url",
            "video",
            "intro",
            "time",
            "people_num",
            "difficulty",
            "recipe_image",
            "recipe_process",
            "like_count",
            "bookmark_count",
            "recipe_comments",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()

    def create(self, validated_data):
        print(123)
        print(validated_data)


class FoodRecipesListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    thumnail_url = serializers.ImageField(source="thumnail", use_url=True)
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()

    class Meta:
        model = FoodRecipes
        fields = [
            "categoryCD",
            "user",
            "title",
            "thumnail_url",
            "intro",
            "like_count",
            "bookmark_count",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()


class ConvenienceRecipesDetailSerializer(serializers.ModelSerializer):
    convenience_items = ConvenienceItemsSerializer(many=True, read_only=True)
    recipe_process = RecipeProcessSerializer(many=True, read_only=True)
    recipe_image = RecipeImageSerializer(many=True, read_only=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    thumnail_url = serializers.ImageField(source="thumnail", use_url=True)
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    tot_price = serializers.ReadOnlyField()

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            "tot_price",
            "thumnail_url",
            "video",
            "intro",
            "time",
            "people_num",
            "difficulty",
            "recipe_image",
            "recipe_process",
            "like_count",
            "bookmark_count",
            "convenience_items",
            "recipe_comments",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()


class ConvenienceRecipesListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    thumnail_url = serializers.ImageField(source="thumnail", use_url=True)
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    tot_price = serializers.ReadOnlyField()

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            "tot_price",
            "thumnail_url",
            "intro",
            "like_count",
            "bookmark_count",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()


class SearchRecipeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
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

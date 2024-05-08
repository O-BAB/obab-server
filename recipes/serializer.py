from rest_framework import serializers

from recipes.models import FoodRecipes, Ingredients, ConvenienceItems, RecipeImage
from recipes.models import RecipeProcess
from comments.serializers import CommentSerializer


class RecipeProcessSerializer(serializers.ModelSerializer):
    process_id = serializers.CharField(source="id", read_only=True)

    class Meta:
        model = RecipeProcess
        fields = ["process_id", "content"]


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = "__all__"


class IngredientsSerializer(serializers.ModelSerializer):
    ingredients_id = serializers.CharField(source="id", read_only=True)

    class Meta:
        model = Ingredients
        fields = ["ingredients_id", "type", "name", "count", "unit", "etc"]


class ConvenienceItemsSerializer(serializers.ModelSerializer):
    convenienceItems_id = serializers.CharField(source="id", read_only=True)

    class Meta:
        model = ConvenienceItems
        fields = ["convenienceItems_id", "name", "price"]


class basicCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # thumnail_url = serializers.ImageField(source="thumnail", use_url=True)
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    recipe_ingredients = IngredientsSerializer(many=True)
    recipe_process = RecipeProcessSerializer(many=True)
    recipe_image = RecipeImageSerializer(many=True, read_only=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "categoryCD",
            "user",
            "title",
            "recipe_ingredients",
            # "thumnail_url",
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
        ingredients_data = validated_data.pop("recipe_ingredients")
        process_datas = validated_data.pop("recipe_process")

        recipe = FoodRecipes.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredients.objects.create(foodrecipe=recipe, **ingredient_data)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=recipe, **process_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("recipe_ingredients")
        process_datas = validated_data.pop("recipe_process")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.recipe_ingredients.all().delete()
        instance.recipe_process.all().delete()

        for ingredient_data in ingredients_data:
            Ingredients.objects.create(foodrecipe=instance, **ingredient_data)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=instance, **process_data)

        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


class ConvenienceCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # thumnail_url = serializers.ImageField(source="thumnail", use_url=True)
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    convenience_items = ConvenienceItemsSerializer(many=True)
    recipe_process = RecipeProcessSerializer(many=True)
    recipe_image = RecipeImageSerializer(many=True, read_only=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            # "thumnail_url",
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

    def create(self, validated_data):
        convenience_items = validated_data.pop("convenience_items")
        process_datas = validated_data.pop("recipe_process")

        tot_price = 0
        for convenience_item in convenience_items:
            tot_price += convenience_item["price"]

        recipe = FoodRecipes.objects.create(**validated_data, tot_price=tot_price)
        for convenience_item in convenience_items:
            ConvenienceItems.objects.create(foodrecipe=recipe, **convenience_item)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=recipe, **process_data)

        return recipe

    def update(self, instance, validated_data):
        convenience_items = validated_data.pop("convenience_items")
        process_datas = validated_data.pop("recipe_process")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.recipe_ingredients.all().delete()
        instance.recipe_process.all().delete()

        for convenience_item in convenience_items:
            ConvenienceItems.objects.create(foodrecipe=instance, **convenience_item)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=instance, **process_data)

        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response


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

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from comments.serializers import CommentSerializer
from recipes.models import ConvenienceItems, FoodRecipes, Ingredients, RecipeProcess


class LikeBookmark:
    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()


class RecipeProcessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = RecipeProcess
        fields = ["id", "order", "content", "image"]


class IngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ingredients
        fields = ["id", "type", "name", "count", "unit", "etc"]


class ConvenienceItemsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ConvenienceItems
        fields = ["id", "name", "price"]


class FoodRecipesSerializer(serializers.ModelSerializer, LikeBookmark):
    like_count = serializers.SerializerMethodField(read_only=True)
    bookmark_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            "thumnail",
            "intro",
            "time",
            "people_num",
            "difficulty",
            "like_count",
            "bookmark_count",
            "created_at",
            "updated_at",
        ]


class BasicRecipeSerializer(serializers.ModelSerializer, LikeBookmark):
    user = serializers.StringRelatedField()
    recipe_ingredients = IngredientsSerializer(many=True)
    recipe_process = RecipeProcessSerializer(many=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    bookmark_count = serializers.SerializerMethodField(read_only=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            "thumnail",
            "video",
            "intro",
            "time",
            "people_num",
            "difficulty",
            "recipe_ingredients",
            "recipe_process",
            "like_count",
            "bookmark_count",
            "created_at",
            "updated_at",
            "recipe_comments",
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop("recipe_ingredients")
        process_datas = validated_data.pop("recipe_process")

        user = self.context.get("request").user

        if isinstance(user, AnonymousUser):
            return print("user not fount")

        validated_data["user"] = user
        recipe = FoodRecipes.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            Ingredients.objects.create(foodrecipe=recipe, **ingredient_data)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=recipe, **process_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("recipe_ingredients", "")
        process_datas = validated_data.pop("recipe_process", "")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for ingredient_data in ingredients_data:
            try:
                ingredient = Ingredients.objects.get(pk=ingredient_data["id"])
                ingredient.type = ingredient_data.get("type", ingredient.type)
                ingredient.name = ingredient_data.get("name", ingredient.name)
                ingredient.count = ingredient_data.get("count", ingredient.count)
                ingredient.unit = ingredient_data.get("unit", ingredient.unit)
                ingredient.etc = ingredient_data.get("etc", ingredient.etc)
                ingredient.save()

            except Ingredients.DoesNotExist:
                Ingredients.objects.create(**ingredient_data)

        for process_data in process_datas:
            try:
                process = RecipeProcess.objects.get(pk=process_data["pk"])
                process.order = process.get("order", process.order)
                process.image = process.get("image", process.image)
                process.content = process.get("content", process.content)
                process.save()

            except RecipeProcess.DoesNotExist:
                RecipeProcess.objects.create(**process_data)

        return instance


class ConvenienceRecipeSerializers(serializers.ModelSerializer, LikeBookmark):
    user = serializers.StringRelatedField()
    convenience_items = ConvenienceItemsSerializer(many=True)
    recipe_process = RecipeProcessSerializer(many=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    bookmark_count = serializers.SerializerMethodField(read_only=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            "thumnail",
            "video",
            "intro",
            "time",
            "difficulty",
            "convenience_items",
            "recipe_process",
            "like_count",
            "bookmark_count",
            "created_at",
            "updated_at",
            "recipe_comments",
        ]

    def create(self, validated_data):
        convenience_items = validated_data.pop("convenience_items")
        process_datas = validated_data.pop("recipe_process")

        user = self.context.get("request").user

        if isinstance(user, AnonymousUser):
            return print("user not fount")

        validated_data["user"] = user
        recipe = FoodRecipes.objects.create(**validated_data)

        for convenience_item in convenience_items:
            Ingredients.objects.create(foodrecipe=recipe, **convenience_item)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=recipe, **process_data)

        return recipe

    def update(self, instance, validated_data):
        convenience_items = validated_data.pop("convenience_items", "")
        process_datas = validated_data.pop("recipe_process", "")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for convenience_item in convenience_items:
            try:
                convenience_item = ConvenienceItems.objects.get(pk=convenience_item["id"])
                convenience_item.name = convenience_item.get("name", convenience_item.name)
                convenience_item.price = convenience_item.get("price", convenience_item.price)
                convenience_item.save()
            except ConvenienceItems.DoesNotExist:
                ConvenienceItems.objects.create(**convenience_item)

        for process_data in process_datas:
            try:
                process = RecipeProcess.objects.get(pk=process_data["pk"])
                process.order = process.get("order", process.order)
                process.image = process.get("image", process.image)
                process.content = process.get("content", process.content)

                process.save()
            except RecipeProcess.DoesNotExist:
                RecipeProcess.objects.create(**process_data)

        return instance


class SearchRecipeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    like_count = serializers.SerializerMethodField()
    thumnail_url = serializers.CharField(source="thumnail")
    bookmark_count = serializers.SerializerMethodField()

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "thumnail_url",
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

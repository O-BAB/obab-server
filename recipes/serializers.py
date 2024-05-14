from django.core.files.storage import default_storage

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
    image_id = serializers.CharField(source="id", read_only=True)
    image_url = serializers.CharField(source="image.url")

    class Meta:
        model = RecipeImage
        fields = ["image_id", "image_url"]


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
    thumnail_url = serializers.CharField(source="thumnail")
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    recipe_ingredients = IngredientsSerializer(many=True)
    recipe_process = RecipeProcessSerializer(many=True)
    recipe_image = RecipeImageSerializer(many=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            "thumnail_url",
            "video",
            "intro",
            "time",
            "people_num",
            "difficulty",
            "recipe_ingredients",
            "recipe_image",
            "recipe_process",
            "like_count",
            "bookmark_count",
            "recipe_comments",
            "created_at",
            "updated_at",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()

    def image_split(self, media_url, recipe):
        try:
            image = RecipeImage.objects.get(image=media_url.replace("/media/", ""))
            image.foodrecipe = recipe
            image.state = "반영"
            image.save()
        except RecipeImage.DoesNotExist:
            print("이미지가 존재하지 않음")

    def create(self, validated_data):
        ingredients_data = validated_data.pop("recipe_ingredients")
        process_datas = validated_data.pop("recipe_process")
        image_datas = validated_data.pop("recipe_image")
        thumnail_url = validated_data.get("thumnail")
        validated_data["thumnail"] = "/media/"+validated_data.get("thumnail")

        recipe = FoodRecipes.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredients.objects.create(foodrecipe=recipe, **ingredient_data)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=recipe, **process_data)
        for image_data in image_datas:
            image_url = image_data.get("image")
            self.image_split(media_url=image_url.get("url"), recipe=recipe)
        self.image_split(media_url=thumnail_url, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("recipe_ingredients")
        process_datas = validated_data.pop("recipe_process")
        image_datas = validated_data.pop("recipe_image")
        thumnail_url = validated_data.get("thumnail")
        validated_data["thumnail"] = "/media/"+validated_data.get("thumnail")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        ConvenienceItems.objects.filter(foodrecipe_id=instance.id).delete()
        RecipeProcess.objects.filter(foodrecipe_id=instance.id).delete()
        RecipeImage.objects.filter(foodrecipe_id=instance.id).update(
            foodrecipe_id=None, state="반영"
        )
        for ingredient_data in ingredients_data:
            Ingredients.objects.create(foodrecipe=instance, **ingredient_data)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=instance, **process_data)
        for image_data in image_datas:
            image_url = image_data.get("image")
            self.image_split(media_url=image_url.get("url"), recipe=instance)
        self.image_split(media_url=thumnail_url, recipe=instance)
        RecipeImage.objects.filter(foodrecipe_id=None, state="반영").delete()
        return instance


class ConvenienceCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    thumnail_url = serializers.CharField(source="thumnail")
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    convenience_items = ConvenienceItemsSerializer(many=True)
    recipe_process = RecipeProcessSerializer(many=True)
    recipe_image = RecipeImageSerializer(many=True)
    recipe_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
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
            "created_at",
            "updated_at",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()

    def image_split(self, media_url, recipe):
        try:
            image = RecipeImage.objects.get(image=media_url.replace("/media/", ""))
            image.foodrecipe = recipe
            image.state = "반영"
            image.save()
        except RecipeImage.DoesNotExist:
            print("이미지가 존재하지 않음")

    def create(self, validated_data):
        convenience_items = validated_data.pop("convenience_items")
        process_datas = validated_data.pop("recipe_process")
        image_datas = validated_data.pop("recipe_image")
        thumnail_url = validated_data.get("thumnail")
        validated_data["thumnail"] = "/media/"+validated_data.get("thumnail")

        tot_price = sum(item["price"] for item in convenience_items)

        recipe = FoodRecipes.objects.create(**validated_data, tot_price=tot_price)
        for convenience_item in convenience_items:
            ConvenienceItems.objects.create(foodrecipe=recipe, **convenience_item)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=recipe, **process_data)
        for image_data in image_datas:
            image_url = image_data.get("image")
            self.image_split(media_url=image_url.get("url"), recipe=recipe)
        self.image_split(media_url=thumnail_url, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        convenience_items = validated_data.pop("convenience_items")
        process_datas = validated_data.pop("recipe_process")
        image_datas = validated_data.pop("recipe_image")
        thumnail_url = validated_data.get("thumnail")
        validated_data["thumnail"] = "/media/"+validated_data.get("thumnail")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        tot_price = 0
        tot_price = sum(item["price"] for item in convenience_items)
        instance.tot_price = tot_price
        instance.save()

        ConvenienceItems.objects.filter(foodrecipe_id=instance.id).delete()
        RecipeProcess.objects.filter(foodrecipe_id=instance.id).delete()
        RecipeImage.objects.filter(foodrecipe_id=instance.id).update(
            foodrecipe_id=None, state="반영"
        )

        for convenience_item in convenience_items:
            ConvenienceItems.objects.create(foodrecipe=instance, **convenience_item)
        for process_data in process_datas:
            RecipeProcess.objects.create(foodrecipe=instance, **process_data)
        for image_data in image_datas:
            image_url = image_data.get("image")
            self.image_split(media_url=image_url.get("url"), recipe=instance)
        self.image_split(media_url=thumnail_url, recipe=instance)
        RecipeImage.objects.filter(foodrecipe_id=None, state="반영").delete()
        return instance


class FoodRecipesListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    thumnail_url = serializers.CharField(source="thumnail")
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()

    class Meta:
        model = FoodRecipes
        fields = [
            "id",
            "categoryCD",
            "user",
            "title",
            "thumnail_url",
            "intro",
            "like_count",
            "bookmark_count",
            "created_at",
            "updated_at",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()


class ConvenienceRecipesListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    thumnail_url = serializers.CharField(source="thumnail")
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
            "created_at",
            "updated_at",
        ]

    def get_like_count(self, obj):
        return obj.like.count()

    def get_bookmark_count(self, obj):
        return obj.bookmark.count()


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


class ImageUploadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RecipeImage
        fields = "__all__"

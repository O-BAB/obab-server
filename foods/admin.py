from django.contrib import admin
from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "food_type",
        "weight",
        "temperature",
        "spicy_level",
        "meat_type",
        "cooking_method",
        "suggestion_user",
    )
    search_fields = (
        "name",
        "food_type",
        "weight",
        "temperature",
        "spicy_level",
        "meat_type",
        "cooking_method",
        "suggestion_user__username",
    )
    list_filter = (
        "food_type",
        "weight",
        "temperature",
        "spicy_level",
        "meat_type",
        "cooking_method",
    )

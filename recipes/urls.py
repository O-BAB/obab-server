from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .viewsets.basicfood_recipes import FoodRecipesViewSet
from .viewsets.convenience_recipes import ConvenienceRecipesViewSet
from .viewsets.broadcast_recipes import BroadcastRecipesViewSet
from .viewsets.seasoning_recipes import SeasoningRecipesViewSet
from .viewsets.ingredients import IngredientsViewset
from .viewsets.recipe_process import RecipeProcessViewset
from .viewsets.convenience_items import ConvenienceItemsViewset
from .viewsets.recipe_images import RecipeImageViewset

router = DefaultRouter()
router.register(r"food-recipes", FoodRecipesViewSet, basename="food-recipes")
router.register(
    r"convenience-recipes", ConvenienceRecipesViewSet, basename="convenience-recipes"
)
router.register(
    r"broadcast-recipes", BroadcastRecipesViewSet, basename="broadcast-recipes"
)
router.register(
    r"seasoning-recipes", SeasoningRecipesViewSet, basename="seasoning_recipe"
)
router.register(
    r"recipes-ingredients", IngredientsViewset, basename="recipe-ingredients"
)
router.register(r"recipes-process", RecipeProcessViewset, basename="recipe-process")
router.register(
    r"convenience-items", ConvenienceItemsViewset, basename="convenience-items"
)
router.register(r"recipe-images", RecipeImageViewset, basename="recipe-images")

# 라우터 URL을 urlpatterns에 추가
urlpatterns = [
    path("", include(router.urls)),
]

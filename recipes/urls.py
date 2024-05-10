from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    basicCreateUpdateView,
    convenienceCreateUpdateView,
    RecipeViewset,
    ImageUploadView,
)

from .views import SearchRecipe

from .views import LikeToggleAPIView, BookmarkToggleAPIView

app_name = "recipes"

router = DefaultRouter()
router.register(r"food-recipes", RecipeViewset, basename="foodrecipe")

urlpatterns = [
    path("recipes/basic", basicCreateUpdateView.as_view(), name="basic-recipes"),
    path(
        "recipes/convenience",
        convenienceCreateUpdateView.as_view(),
        name="convenience-recipes",
    ),
    path("recipes/images", ImageUploadView.as_view(), name="recipe-images"),
    path("recipes/", include(router.urls)),
    path("recipes/like-toggle/", LikeToggleAPIView.as_view()),
    path("recipes/bookmark-toggle/", BookmarkToggleAPIView.as_view()),
    path("search", SearchRecipe.as_view()),
]

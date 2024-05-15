from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    basicCreateView,
    basicUpdateView,
    convenienceCreateView,
    convenienceUpdateView,
    RecipeViewset,
    ImageUploadView,
)

from .views import SearchRecipe

from .views import LikeToggleAPIView, BookmarkToggleAPIView

app_name = "recipes"

router = DefaultRouter()
router.register(r"food-recipes", RecipeViewset, basename="foodrecipe")

urlpatterns = [
    path("recipes/basic", basicCreateView.as_view(), name="basic-recipes-create"),
    path(
        "recipes/basic/<int:id>/",
        basicUpdateView.as_view(),
        name="basic-recipes-update",
    ),
    path(
        "recipes/convenience",
        convenienceCreateView.as_view(),
        name="convenience-recipes-create",
    ),
    path(
        "recipes/convenience/<int:id>/",
        convenienceUpdateView.as_view(),
        name="convenience-recipes-update",
    ),
    path("recipes/images", ImageUploadView.as_view(), name="recipe-images"),
    path("recipes/", include(router.urls)),
    path("recipes/like-toggle/", LikeToggleAPIView.as_view()),
    path("recipes/bookmark-toggle/", BookmarkToggleAPIView.as_view()),
    path("search", SearchRecipe.as_view()),
]

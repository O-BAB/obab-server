from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookmarkToggleAPIView, LikeToggleAPIView, SearchRecipe
from .viewsets import (
    ImageUploadView,
    RecipeViewset,
    basicCreateView,
    basicUpdateView,
    convenienceCreateView,
    convenienceUpdateView,
)

app_name = "recipes"

router = DefaultRouter()
router.register(r"food-recipes", RecipeViewset, basename="foodrecipe")

urlpatterns = [
    path("recipes/basic", basicCreateView.as_view(), name="basic-recipes-create"),
    path("recipes/basic/<int:id>/", basicUpdateView.as_view(), name="basic-recipes-update"),
    path("recipes/convenience", convenienceCreateView.as_view(), name="convenience-recipes-create"),
    path("recipes/convenience/<int:id>/", convenienceUpdateView.as_view(), name="convenience-recipes-update"),
    path("recipes/images", ImageUploadView.as_view(), name="recipe-images"),
    path("recipes/", include(router.urls)),
    path("recipes/like-toggle/", LikeToggleAPIView.as_view()),
    path("recipes/bookmark-toggle/", BookmarkToggleAPIView.as_view()),
    path("search", SearchRecipe.as_view()),
]

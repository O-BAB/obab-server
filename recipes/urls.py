from rest_framework.routers import SimpleRouter
from rest_framework.urls import path

from recipes.viewsets import FoodrecipeViewsets

from .views import BookmarkToggleAPIView, LikeToggleAPIView, SearchRecipe

app_name = "recipes"

router = SimpleRouter(trailing_slash=False)

recipeurls = [
    path("recipes/list", FoodrecipeViewsets.as_view({"get": "list"})),
    path("recipes/<str:category>-list", FoodrecipeViewsets.as_view({"get": "list"})),
    path("recipes/<int:pk>", FoodrecipeViewsets.as_view({"get": "retrieve", "delete": "destroy"})),
    path("recipes/basic", FoodrecipeViewsets.as_view({"post": "create_basic"})),
    path("recipes/basic/<int:pk>", FoodrecipeViewsets.as_view({"patch": "partial_basic"})),
    path("recipes/convenience", FoodrecipeViewsets.as_view({"post": "create_convenience"})),
    path("recipes/convenience/<int:pk>", FoodrecipeViewsets.as_view({"patch": "partial_convenience"})),
]

urlpatterns = [
    path("recipes/like-toggle/", LikeToggleAPIView.as_view()),
    path("recipes/bookmark-toggle/", BookmarkToggleAPIView.as_view()),
    path("search", SearchRecipe.as_view()),
    *recipeurls,
]

from django.urls import path
from .viewsets import RecipeDetail, RecipeListView
from .views import SearchRecipe

from .views import LikeToggleAPIView, BookmarkToggleAPIView

urlpatterns = [
    path("recipes/", RecipeListView.as_view()),
    path("recipes/<int:recipe_id>/", RecipeDetail.as_view()),
    path("recipes/like-toggle/", LikeToggleAPIView.as_view()),
    path("recipes/bookmark-toggle/", BookmarkToggleAPIView.as_view()),
    path("search", SearchRecipe.as_view()),
]

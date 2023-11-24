from django.urls import path

from foods.views import SearchFood


urlpatterns = [
    path("search/", SearchFood.as_view(), name="search"),
]

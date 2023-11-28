from django.urls import path

from foods.views import SearchFood
# from . import functions

urlpatterns = {
    path("search/", SearchFood.as_view(), name="search"),
    # path('askopenai/', functions.ask_openai, name='opengpt'),
}

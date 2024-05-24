from django.urls import path

from .views import OpenAIView

urlpatterns = [path("", OpenAIView.as_view(), name="query_view")]

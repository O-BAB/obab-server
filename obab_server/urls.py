from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from obab_server.swagger import get_swagger_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("recipes.urls")),
    path("accounts/", include("accounts.urls")),
    path("comments/", include("comments.urls")),
    path("openai/", include("menu.urls")),
]

urlpatterns += get_swagger_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

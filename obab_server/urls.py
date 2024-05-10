from django.contrib import admin
from django.urls import path, include
from obab_server.swagger import get_swagger_urls

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("recipes.urls")),
    path("accounts/", include("accounts.urls")),
    path("comments/", include("comments.urls")),
]

urlpatterns += get_swagger_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

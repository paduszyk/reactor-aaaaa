from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

__all__ = ["urlpatterns"]

# Project-level paths

urlpatterns = []


# Included from apps

urlpatterns += [
    path("admin/", admin.site.urls),
]


# Internationalization

urlpatterns += [
    path("i18n/", include("django.conf.urls.i18n")),
]


# Static files and media

urlpatterns = (
    urlpatterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

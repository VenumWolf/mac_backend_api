from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from config.settings.base import ADMIN_SITE_PATH

urlpatterns = [
    path(ADMIN_SITE_PATH, admin.site.urls),
    path("api/", include("config.api_router")),
]

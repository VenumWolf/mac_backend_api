from django.contrib import admin
from django.urls import path

from config.settings.base import ADMIN_SITE_PATH

urlpatterns = [
    path(ADMIN_SITE_PATH, admin.site.urls),
]

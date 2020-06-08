from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from config.settings.base import ADMIN_SITE_PATH

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path(ADMIN_SITE_PATH, admin.site.urls),
]

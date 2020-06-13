from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from config.settings.base import ADMIN_SITE_PATH

urlpatterns = [
    path(ADMIN_SITE_PATH, admin.site.urls),
    path('api/authentication/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/authentication/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/", include("config.api_router")),
    path("", RedirectView.as_view(url="/api/"), name="index")
]

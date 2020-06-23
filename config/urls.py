from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)

from config.settings.base import ADMIN_SITE_PATH

urlpatterns = [
    path(ADMIN_SITE_PATH, admin.site.urls),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/audio/", include("mac_backend_api.audio.urls")),
    path("api/", include("config.api_router")),
    path("", RedirectView.as_view(url="/api/"), name="index")
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

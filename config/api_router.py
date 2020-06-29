from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from mac_backend_api.audio.api.views import AudioViewSet
from mac_backend_api.users.api.views import UserViewSet

app_name = "api"

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("audio", AudioViewSet)

urlpatterns = [
]

urlpatterns = urlpatterns + router.urls

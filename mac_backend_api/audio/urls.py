from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mac_backend_api.audio.api.views import AudioViewSet

router = DefaultRouter()
router.register("", AudioViewSet, basename="audio")

urlpatterns = [
    path("", include(router.urls))
]

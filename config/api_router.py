from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mac_backend_api.users.api.views import UserViewSet
from mac_backend_api.audio.api.views import AudioViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("audio", AudioViewSet)

app_name = "api"
urlpatterns = router.urls

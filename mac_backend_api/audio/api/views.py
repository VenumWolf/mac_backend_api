from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from mac_backend_api.audio.api.serializers import AudioSerializer
from mac_backend_api.audio.models import Audio


class AudioViewSet(ModelViewSet):
    serializer_class = AudioSerializer
    lookup_field = "pk"
    queryset = Audio.objects.all()

    def filter_queryset(self, queryset):
        if self.action == "list":
            queryset = queryset.filter(is_public=True)
        return queryset

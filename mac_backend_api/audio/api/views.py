from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics

from mac_backend_api.audio.api.serializers import AudioSerializer
from mac_backend_api.audio.models import Audio


class AudioViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = AudioSerializer
    queryset = Audio.objects.filter(is_public=True)
    lookup_field = "id"


class AudioBaseView:
    queryset = Audio.objects.filter(is_public=True)
    serializer_class = AudioSerializer


class AudioListView(AudioBaseView, generics.ListCreateAPIView):
    pass


class AudioDetailView(AudioBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass

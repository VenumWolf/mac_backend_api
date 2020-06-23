from rest_framework import generics

from mac_backend_api.audio.api.serializers import AudioSerializer
from mac_backend_api.audio.models import Audio


class AudioBaseView:
    queryset = Audio.objects.filter(is_public=True)
    serializer_class = AudioSerializer


class AudioListView(AudioBaseView, generics.ListCreateAPIView):
    pass


class AudioDetailView(AudioBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass

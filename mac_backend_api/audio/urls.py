from django.urls import path

from mac_backend_api.audio.api.views import AudioListView, AudioDetailView

app_name = 'audio'

urlpatterns = [
    path("<uuid:id>", AudioDetailView.as_view(), name="audio-detail"),
    path("", AudioListView.as_view(), name="audio-list")
]

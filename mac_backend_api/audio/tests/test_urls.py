import pytest
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from mac_backend_api.audio.models import Audio


@pytest.mark.django_db
class TestUrls:
    def test_audio_detail(self):
        audio = mixer.blend(Audio)
        assert reverse("audio:audio-detail", kwargs={"id": audio.id}) == f"/api/audio/{audio.id}/"
        assert resolve(f"/api/audio/{audio.id}/").view_name == "audio:audio-detail"

    def test_audio_list(self):
        assert reverse("audio:audio-list") == "/api/audio/"
        assert resolve("/api/audio/list/").view_name == "audio:audio-list"


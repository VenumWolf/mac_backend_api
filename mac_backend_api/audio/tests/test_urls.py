import pytest
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from mac_backend_api.audio.models import Audio


@pytest.mark.django_db
class TestUrls:
    def test_audio_detail(self):
        audio = mixer.blend(Audio)
        assert reverse("api:audio-detail", kwargs={"pk": audio.id}) == f"/api/audio/{audio.id}/"
        assert resolve(f"/api/audio/{audio.id}/").view_name == "api:audio-detail"

    def test_audio_list(self):
        assert reverse("api:audio-list") == "/api/audio/"
        assert resolve("/api/audio/").view_name == "api:audio-list"


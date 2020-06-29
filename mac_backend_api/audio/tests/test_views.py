import json

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from mixer.backend.django import mixer

from mac_backend_api.audio.models import Audio


class TestAudioViewSet(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio, is_public=True)
        self.client = Client()

    def test_list(self):
        response = self.client.get(reverse("api:audio-list"))
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_detail_get(self):
        response = self.client.get(reverse("api:audio-detail", kwargs={"id": self.audio.id}))
        assert response.status_code == 200
        TestAudioViewSet.__verify_audio_matches_data(self.audio, response.data)

    def test_detail_put(self):
        response = self.client.put(
            reverse("api:audio-detail", kwargs={"id": self.audio.id}),
            data="title=Hello%2C%20World%21",
            content_type="application/x-www-form-urlencoded",
        )
        assert response.status_code == 200
        assert Audio.objects.get(id=self.audio.id).title == "Hello, World!"

    def test_detail_patch(self):
        response = self.client.put(
            reverse("api:audio-detail", kwargs={"id": self.audio.id}),
            data="title=Hello%2C%20World%21",
            content_type="application/x-www-form-urlencoded",
        )
        assert response.status_code == 200
        assert Audio.objects.get(id=self.audio.id).title == "Hello, World!"

    def test_detail_delete(self):
        audio = mixer.blend(Audio)
        response = self.client.delete(reverse("api:audio-detail", kwargs={"id": audio.id}))
        assert response.status_code == 204

    @staticmethod
    def __verify_audio_matches_data(audio, data):
        assert data == {
            "id": str(audio.id),
            "title": audio.title,
            "slug": audio.slug,
            "description": audio.description,
            "listen_count": audio.listen_count,
            "uploaded_at": audio.uploaded_at.strftime(settings.DATETIME_FORMAT),
            "is_public": audio.is_public,
            "url": f"http://testserver{audio.get_absolute_url()}"
        }

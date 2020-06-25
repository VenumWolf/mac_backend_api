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
        assert response.data == {
            "id": str(self.audio.id),
            "title": self.audio.title,
            "slug": self.audio.slug,
            "description": self.audio.description,
            "listen_count": self.audio.listen_count,
            "uploaded_at": self.audio.uploaded_at.strftime(settings.DATETIME_FORMAT),
            "is_public": self.audio.is_public,
            "url": f"http://testserver{self.audio.get_absolute_url()}"
        }

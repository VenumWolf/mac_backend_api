import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

from mac_backend_api.audio.models import Audio, Author


User = get_user_model()


@pytest.mark.django_db
class TestAudioModel(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio)
        self.audio.views = 0

    def test_get_url(self) -> None:
        assert self.audio.get_absolute_url() == f"/api/audio/{self.audio.id}/"

    def test_add_listen(self) -> None:
        self.audio.add_listen()
        assert self.audio.listen_count == 1

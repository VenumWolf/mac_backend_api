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
        self.audio_author_user_1 = mixer.blend(User)
        self.audio_author_1 = mixer.blend(Author, user=self.audio_author_user_1, audio=self.audio)
        self.audio_author_user_2 = mixer.blend(User)
        self.audio_author_2 = mixer.blend(Author, user=self.audio_author_user_2, audio=self.audio)

    def test_get_url(self) -> None:
        assert self.audio.get_absolute_url() == f"/api/audio/{self.audio.id}/"

    def test_get_authors(self) -> None:
        assert set(self.audio.get_authors()) == {self.audio_author_1, self.audio_author_2}

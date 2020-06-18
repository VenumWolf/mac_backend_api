import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

from mac_backend_api.audio.models import Audio, Author, Like

User = get_user_model()


@pytest.mark.django_db
class TestAudioModel(TestCase):
    def setUp(self) -> None:
        self.__blend_audio_and_author()
        self.like_user = mixer.blend(User)

    def test_get_url(self) -> None:
        """Ensures the audio url is what is expected"""
        assert self.audio.get_absolute_url() == f"/api/audio/{self.audio.id}/"

    def test_add_listen(self) -> None:
        """Ensures the Audio's add_listen method adds 1 listen"""
        self.audio.add_listen()
        assert self.audio.listen_count == 1

    def test_like_count(self) -> None:
        """Ensures the Audio's like_count property finds and counts its likes"""
        like = mixer.blend(Like)
        like.user = self.like_user
        like.audio = self.audio
        like.save()
        assert self.audio.like_count == 1
        like.delete()

    def test_like_count_with_other_likes_present(self):
        """Ensures the Audio's like_count property only counts likes referencing itself"""
        mixer.blend(Like)
        assert self.audio.like_count == 0

    def __blend_audio_and_author(self) -> None:
        self.audio = mixer.blend(Audio)
        self.author = mixer.blend(Author)
        self.user = mixer.blend(User)
        self.audio.authors.add(self.author)
        self.audio.views = 0
        self.audio.save()

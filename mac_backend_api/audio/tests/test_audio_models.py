import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

from mac_backend_api.audio.exceptions import UserAlreadyLikesException
from mac_backend_api.audio.models import Audio, AudioStream, Author, Like, get_audio_stream_upload_path

User = get_user_model()


@pytest.mark.django_db
class TestAudioModel(TestCase):
    def setUp(self) -> None:
        self.__blend_audio_and_author()
        self.like_user = mixer.blend(User)

    def test_get_url(self) -> None:
        """Ensures the audio url is what is expected"""
        assert self.audio.get_absolute_url() == f"/api/audio/{self.audio.id}"

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

    def test_add_like(self):
        """Ensures likes are added correctly"""
        user = mixer.blend(User)
        self.audio.add_like(user)
        assert self.audio.like_set.get(user=user).user == user

    def test_add_double_like(self):
        """Ensures subsequent attempts to like don't raise exceptions"""
        user = mixer.blend(User)
        self.audio.add_like(user)
        self.audio.add_like(user)
        assert self.audio.like_set.get(user=user).user == user

    def test_remove_like(self):
        """Ensures likes are removed correctly"""
        user = mixer.blend(User)
        self.audio.add_like(user)
        self.audio.remove_like(user)
        assert len(self.audio.like_set.filter(user=user)) == 0

    def test_remove_nonexistent_like(self):
        """Ensures subsequent attempts to unlike don't raise exceptions"""
        user = mixer.blend(User)
        self.audio.add_like(user)
        self.audio.remove_like(user)
        self.audio.remove_like(user)
        assert len(self.audio.like_set.filter(user=user)) == 0

    def __blend_audio_and_author(self) -> None:
        self.audio = mixer.blend(Audio)
        self.author = mixer.blend(Author)
        self.user = mixer.blend(User)
        self.audio.authors.add(self.author)
        self.audio.views = 0
        self.audio.save()


@pytest.mark.django_db
class TestAudioStreamModel(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio)
        self.audio_stream = mixer.blend(AudioStream, audio=self.audio)

    def test_get_audio_stream_upload_path(self):
        assert (get_audio_stream_upload_path(self.audio_stream, "fake-file-name")
                == f"audio/{self.audio_stream.audio.id}/{self.audio_stream.id}.{self.audio_stream.format}")


@pytest.mark.django_db
class TestLikes(TestCase):
    def setUp(self) -> None:
        self.like_user = mixer.blend(User)
        self.like_audio = mixer.blend(Audio)
        self.__blend_like()

    def test_create_new_like(self) -> None:
        """Ensures likes can be created"""
        new_like = mixer.blend(Like)
        new_like.audio = self.like_audio
        new_like.save()

    def test_create_double_like(self):
        """Ensures a user cannot like an audio more than once"""
        with pytest.raises(UserAlreadyLikesException, match=r".* already likes *."):
            new_like = Like(
                user=self.like_user,
                audio=self.like_audio,
            )
            new_like.save()

    def __blend_like(self):
        self.like = mixer.blend(Like)
        self.like.user = self.like_user
        self.like.audio = self.like_audio
        self.like.save()

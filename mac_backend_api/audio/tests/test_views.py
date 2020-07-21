#  Copyright (C) 2020  Mind Audio Central
#
#  This file is part of mac_backend_api.
#
#  mac_backend_api is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  mac_backend_api is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with mac_backend_api.  If not, see <https://www.gnu.org/licenses/>.

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from mixer.backend.django import mixer

from mac_backend_api.audio.models import Audio, Stream


class TestAudioViewSet(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio, is_public=True)
        self.stream = mixer.blend(Stream, audio=self.audio)
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
        assert data.get("id") == str(audio.id)
        assert data.get("title") == audio.title
        assert data.get("slug") == audio.slug
        assert data.get("description") == audio.description
        assert data.get("listen_count") == audio.listen_count
        assert data.get("uploaded_at") == audio.uploaded_at.strftime(settings.DATETIME_FORMAT)
        assert data.get("is_public") == audio.is_public
        assert data.get("url") == f"http://testserver{audio.get_absolute_url()}"
        assert data.get("streams") is not None  # Audio tests do not need to verify this, but it should never be None.


class TestStreamViewSet(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio)
        self.stream = mixer.blend(Stream, audio=self.audio)
        self.client = Client()

    def test_list(self):
        response = self.client.get(reverse("api:stream-list"))
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_detail_get(self):
        response = self.client.get(reverse("api:stream-detail", kwargs={"id": self.stream.id}))
        assert response.status_code == 200
        TestStreamViewSet.__verify_stream_matches_data(self.stream, response.data)

    @staticmethod
    def __verify_stream_matches_data(stream, data):
        assert data.get("id") == str(stream.id)
        assert data.get("url") == f"http://testserver{stream.get_absolute_url()}"
        assert data.get("audio") == f"http://testserver{stream.audio.get_absolute_url()}"
        assert data.get("format") == stream.format
        assert data.get("bit_rate") == stream.bit_rate
        assert data.get("sample_rate") == stream.sample_rate
        assert data.get("allow_downloads") == stream.allow_downloads
        assert data.get("file") == f"http://testserver/media/{stream.file.name}"

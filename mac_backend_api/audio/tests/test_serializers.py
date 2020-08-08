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

from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from mac_backend_api.audio.api.serializers import AudioSerializer, StreamSerializer, NestedStreamSerializer
from mac_backend_api.audio.models import Audio, Stream


class TestAudioSerializer(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio)
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get("/")
        self.serialized_audio = AudioSerializer(self.audio, context={"request": self.request})

    def test_fields(self) -> None:
        assert list(self.serialized_audio.data.keys()) == ["id", "title", "slug", "url", "description", "listen_count",
                                                           "uploaded_at", "is_public", "authors", "streams", "file"]


class TestStreamSerializer(TestCase):
    def setUp(self) -> None:
        self.stream = mixer.blend(Stream)
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get("/")
        self.serialized_stream = StreamSerializer(self.stream, context={"request": self.request})

    def test_fields(self) -> None:
        assert list(self.serialized_stream.data.keys()) == ["id", "url", "audio", "format", "bit_rate", "sample_rate",
                                                            "allow_downloads", "file"]


class TestEmbeddedStreamSerializer(TestCase):
    def setUp(self) -> None:
        self.stream = mixer.blend(Stream)
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get("/")
        self.serialized_stream = NestedStreamSerializer(self.stream, context={"request": self.request})

    def test_fields(self) -> None:
        assert list(self.serialized_stream.data.keys()) == ["id", "url", "format", "bit_rate", "sample_rate",
                                                            "allow_downloads", "file"]

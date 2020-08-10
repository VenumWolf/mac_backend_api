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
from mac_backend_api.audio.tests.test_views import TEST_FILE


class TestAudioSerializer(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio)
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get("/")
        self.serialized_audio = AudioSerializer(self.audio, context={"request": self.request})

    def test_fields(self) -> None:
        assert list(self.serialized_audio.data.keys()) == ["id", "title", "url", "description", "listen_count",
                                                           "uploaded_at", "is_public", "authors", "streams"]

    def test_stream_creation(self) -> None:
        """Verifies the required streams are created."""
        serializer = AudioSerializer(data={
            "title": "test",
            "description": "test",
            "is_public": True,
            "file": TEST_FILE
        })
        serializer.is_valid()
        audio = serializer.save()
        self.assertEquals(len(audio.streams.all()), 3, msg="There should be 3 streams associated with the Audio")
        self.assertEquals(len(audio.streams.filter(bit_rate=Stream.AudioBitRate.HIGH)), 1)
        self.assertEquals(len(audio.streams.filter(bit_rate=Stream.AudioBitRate.AVERAGE)), 1)
        self.assertEquals(len(audio.streams.filter(bit_rate=Stream.AudioBitRate.LOW)), 1)


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

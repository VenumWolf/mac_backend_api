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
import json

from django.test import TestCase, RequestFactory
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from django.conf import settings
from mac_backend_api.audio.api.serializers import AudioSerializer, StreamSerializer
from mac_backend_api.audio.models import Audio, Stream


class TestAudioSerializer(TestCase):
    def setUp(self) -> None:
        self.audio = mixer.blend(Audio)
        self.request_factory = APIRequestFactory()
        self.request = self.request_factory.get("/")
        self.serialized_audio = AudioSerializer(self.audio, context={"request": self.request})

    def test_fields(self) -> None:
        assert list(self.serialized_audio.data.keys()) == ["id", "title", "slug", "url", "description", "listen_count",
                                                           "uploaded_at", "is_public", "authors", "streams"]


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

import pytest
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from mac_backend_api.audio.models import Audio, Stream


@pytest.mark.django_db
class TestAudioUrls:
    def test_audio_detail(self):
        audio = mixer.blend(Audio)
        assert reverse("api:audio-detail", kwargs={"id": audio.id}) == f"/api/audio/{audio.id}/"
        assert resolve(f"/api/audio/{audio.id}/").view_name == "api:audio-detail"

    def test_audio_list(self):
        assert reverse("api:audio-list") == "/api/audio/"
        assert resolve("/api/audio/").view_name == "api:audio-list"


@pytest.mark.django_db
class TestStreamUrls:
    def test_stream_detail(self):
        stream = mixer.blend(Stream)
        assert reverse("api:stream-detail", kwargs={"id": stream.id}) == f"/api/stream/{stream.id}/"
        assert resolve(f"/api/stream/{stream.id}/").view_name == "api:stream-detail"

    def test_audio_list(self):
        assert reverse("api:stream-list") == "/api/stream/"
        assert resolve("/api/stream/").view_name == "api:stream-list"

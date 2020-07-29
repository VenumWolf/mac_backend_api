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
from rest_framework.test import APIRequestFactory

from mac_backend_api.audio.api.views import AudioViewSet
from mac_backend_api.audio.models import Audio, Stream


def blend_audio(count=1):
    """
    A helper method for creating audios.
    :param count: The number of audios to blend.
    :return:      An Audio instance if count = 1, or a list of Audio instances if count > 1.
    """
    if count == 1:
        audio = mixer.blend(Audio)
    elif count > 1:
        audio = list()
        for i in range(count):
            audio.append(mixer.blend(Audio))
    else:
        audio = list()
    return audio


class TestAudioViewSet(TestCase):
    def setUp(self) -> None:
        self.view_set = AudioViewSet
        self.request_factory = APIRequestFactory()

    def test_get_detail_view(self) -> None:
        """Verifies the AudioViewSet's detail view returns with status code 200 when provided a valid id."""
        audio = blend_audio()
        request = self.request_factory.get("")
        audio_detail_view = self.view_set.as_view({"get": "retrieve"})
        response = audio_detail_view(request, id=audio.id)
        self.assertEquals(response.status_code, 200)

    def test_get_detail_view_invalid_id(self) -> None:
        """Verifies the AudioViewSet's detail view returns a 404 when provided an invalid id."""
        request = self.request_factory.get("")
        audio_detail_view = self.view_set.as_view({"get": "retrieve"})
        response = audio_detail_view(request, id="invalid")
        self.assertEquals(response.status_code, 404)

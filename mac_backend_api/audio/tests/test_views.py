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
from io import BytesIO

from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from mac_backend_api.audio.api.views import AudioViewSet, StreamViewSet
from mac_backend_api.audio.models import Audio, Stream

TEST_FILE = BytesIO(b"contents")
TEST_FILE.name = "test_file.ogg"


def blend_audio(count=1):
    """
    A helper method for creating audios.  By Default the audio is unlisted (is_public=False), call
    make_public(blend_audio()) to generate public audios.
    :param count: The number of audios to blend.
    :return:      An Audio instance if count = 1, or a list of Audio instances if count > 1.
    """
    if count == 1:
        audio = mixer.blend(Audio, is_public=False)
    elif count > 1:
        audio = list()
        for i in range(count):
            audio.append(mixer.blend(Audio, is_public=False))
    else:
        audio = list()
    return audio


def make_public(audio) -> None:
    """
    Set an Audio instance's visibility to public.
    :param audio: The Audio instance to make public.
    :return:      The Audio instance if audio is an Audio, or a list of length = 1, or a list of Audio instances if
                  audio is a list of length > 1.
    """
    if not isinstance(audio, list):
        audio = [audio]
    for audio_instance in audio:
        audio_instance.is_public = True
        audio_instance.save()
    if len(audio) == 1:
        audio = audio[0]
    return audio


class TestAudioViewSet(TestCase):
    def setUp(self) -> None:
        self.view_set = AudioViewSet
        self.request_factory = APIRequestFactory()
        self.data = {
            "title": "Hello, world!",
            "description": "This is a test."
        }

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

    def test_put_detail_view_new_audio(self) -> None:
        """Verifies the AudioViewSet's detail view creates new Audio through a put request."""
        request = self.request_factory.put("", data=self.data, format="json")
        update_view = self.view_set.as_view({"put": "create"})
        response = update_view(request)
        self.assertEquals(response.status_code, 201)

    def test_put_detail_view_existing_audio(self) -> None:
        """Verifies the AudioViewSet's detail view updates existing Audio with a put request."""
        audio = blend_audio()
        request = self.request_factory.put("", data=self.data, format="json")
        update_view = self.view_set.as_view({"put": "update"})
        response = update_view(request, id=audio.id)
        self.assertEquals(response.status_code, 200)

    def test_patch_detail_view(self) -> None:
        """Verifies the AudioViewSet's detail view updates existing Audio with a patch request."""
        audio = blend_audio()
        request = self.request_factory.patch("", data=self.data, format="json")
        update_view = self.view_set.as_view({"patch": "partial_update"})
        response = update_view(request, id=audio.id)
        self.assertEquals(response.status_code, 200)

    def test_delete_detail_view(self) -> None:
        """Verifies the AudioViewSet's detail view delete's existing audio with a delete request."""
        audio = blend_audio()
        request = self.request_factory.delete("")
        update_view = self.view_set.as_view({"delete": "destroy"})
        response = update_view(request, id=audio.id)
        self.assertEquals(response.status_code, 204)

    def test_get_list_view(self) -> None:
        """Verifies the AudioViewSet's list view data contains only public audio."""
        blend_audio(10)
        make_public(blend_audio(10))
        request = self.request_factory.get("")
        list_view = self.view_set.as_view({"get": "list"})
        response = list_view(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 10)


def blend_stream(count=1):
    """
    A helper method for creating streams.
    :param count: The number of streams to blend.
    :return:      A Stream instance if count = 1, or a list of Stream instances if count > 1.
    """
    if count == 1:
        stream = mixer.blend(Stream)
    elif count > 1:
        stream = list()
        for i in range(count):
            stream.append(mixer.blend(Stream))
    else:
        stream = list()
    return stream


class TestStreamViewSet(TestCase):
    def setUp(self) -> None:
        self.view_set = StreamViewSet
        self.request_factory = APIRequestFactory()
        self.file = TEST_FILE
        self.data = {
            "format": "ogg",
            "bit_rate": 192000,
            "sample_rate": 48000,
            "allow_downloads": False,
        }

    def get_detail_view(self) -> None:
        """Verifies the detail view returns a status code 200 when provided a valid id."""
        stream = blend_stream()
        request = self.request_factory.get("")
        detail_view = self.view_set.as_view({"get": "retrieve"})
        response = detail_view(request, id=stream.id)
        self.assertEquals(response.status_code, 200)

    def test_get_detail_view_invalid_id(self) -> None:
        """Verifies the detail view returns a 404 when provided an invalid id."""
        request = self.request_factory.get("")
        detail_view = self.view_set.as_view({"get": "retrieve"})
        response = detail_view(request, id="invalid")
        self.assertEquals(response.status_code, 404)

    def test_put_detail_view_new_stream(self) -> None:
        """Verifies the detail view creates new Audio through a PUT request."""
        data = self.data
        data["audio"] = blend_audio().get_absolute_url()
        data["file"] = self.file
        request = self.request_factory.put("", data=data, format="multipart")
        update_view = self.view_set.as_view({"put": "create"})
        response = update_view(request)
        print(response.data)
        self.assertEquals(response.status_code, 201)

    def test_put_detail_view_existing_stream(self) -> None:
        """Verifies the detail view updates existing Audio with a PUT request."""
        stream = blend_stream()
        request = self.request_factory.put("", data=self.data, format="json")
        update_view = self.view_set.as_view({"put": "update"})
        response = update_view(request, id=stream.id)
        self.assertEquals(response.status_code, 200)

    def test_patch_detail_view(self) -> None:
        """Verifies the detail view updates existing Audio with a PATCH request."""
        stream = blend_stream()
        request = self.request_factory.patch("", data=self.data, format="json")
        update_view = self.view_set.as_view({"patch": "partial_update"})
        response = update_view(request, id=stream.id)
        self.assertEquals(response.status_code, 200)

    def test_delete_detail_view(self) -> None:
        """Verifies the detail view delete's existing audio with a DELETE request."""
        stream = blend_stream()
        request = self.request_factory.delete("")
        update_view = self.view_set.as_view({"delete": "destroy"})
        response = update_view(request, id=stream.id)
        self.assertEquals(response.status_code, 204)

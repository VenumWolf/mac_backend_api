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

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from mac_backend_api.audio.api.views import AudioViewSet, StreamViewSet
from mac_backend_api.audio.models import Audio, Stream

User = get_user_model()

TEST_FILE_BYTES = BytesIO(b'content')
TEST_FILE = InMemoryUploadedFile(file=TEST_FILE_BYTES, field_name="file", name="uploaded",
                                 size=len(TEST_FILE_BYTES.read()), charset=None, content_type="audio/ogg")


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


def blend_user(permission_names=None) -> User:
    """
    A helper method for creating users for testing.
    :param permission_names: A permission, if any the user should have. Default is None.  May be a String, or a List.
    :return:                A user with the permission if one is provided.
    """
    user = mixer.blend(User)
    if permission_names is not None:
        if not isinstance(permission_names, list):
            permission_names = [permission_names]
        for permission in permission_names:
            permission = Permission.objects.get(name=permission)
            user.user_permissions.add(permission)
    return user


class TestAudioViewSet(TestCase):
    def setUp(self) -> None:
        self.view_set = AudioViewSet
        self.request_factory = APIRequestFactory()
        self.file = TEST_FILE_BYTES
        self.data = {
            "title": "Hello, world!",
            "description": "This is a test."
        }

    def test_list_view(self) -> None:
        """Verify the list view returns a 200 for unauthenticated users."""
        response = self.make_get_request(view_name="list")
        self.assertEquals(response.status_code, 200, msg=response.data)

    def test_retrieve_view(self) -> None:
        """Verify the retrieve view returns a 200 for unauthenticated users when provided a valid id."""
        response = self.make_get_request(view_name="retrieve", audio=blend_audio())
        self.assertEquals(response.status_code, 200, msg=response.data)

    def make_get_request(self, view_name, audio=None, user=None) -> Response:
        """
        Make a get request to the specified view and return its response.
        :param view_name: The view to which to make the request.
        :param audio:     The audio to request if any.  Default is None.
        :param user:      The user making the request if any.  Default is None.
        :return:          The Response from the view.
        """
        view = self.view_set.as_view({"get": view_name})
        request = self.request_factory.get("")
        if user is not None:
            force_authenticate(request, user)
            request.user = user
        if audio is not None:
            response = view(request, id=audio.id)
        else:
            response = view(request)
        return response

    def test_create_view(self) -> None:
        """Verify the create view returns a 201 when provided a file and valid data."""
        response = self.make_create_request(audio_file=TEST_FILE, user=blend_user("Can add audio"))
        self.assertEquals(response.status_code, 201, msg=response.data)

    def test_create_view_without_file(self) -> None:
        """Verify the create view returns a 400 with a 'file_not_provided' error message when a file is not provided."""
        response = self.make_create_request(user=blend_user("Can add audio"))
        self.assertEquals(response.status_code, 400, msg=response.data)

    def test_create_view_no_permission(self) -> None:
        """Verify the create view returns a 403 when the user is missing permissions."""
        response = self.make_create_request(audio_file=TEST_FILE, user=blend_user())
        self.assertEquals(response.status_code, 403, msg=response.data)

    def test_create_view_no_user(self) -> None:
        """Verify the create view returns a 401 when user is unauthenticated."""
        response = self.make_create_request(audio_file=TEST_FILE)
        self.assertEquals(response.status_code, 401, msg=response.data)

    def make_create_request(self, audio_file=None, user=None) -> Response:
        """
        Make a request to the create view and return its response.
        :param audio_file: The audio file to attach with the request if any.  Default is None
        :param user:       The user making the request if any.  Default is None.
        :return:           The Response from the view.
        """
        view = self.view_set.as_view({"post": "create"})
        request = self.request_factory.post("", data=self.data, format="multipart")
        if audio_file is not None:
            request.FILES["file"] = TEST_FILE
        if user is not None:
            force_authenticate(request, user)
            request.user = user
        return view(request)

    def test_update_view_no_permission(self) -> None:
        """Verify the update view returns a 403 when the user is missing permissions."""
        response = self.make_update_request(audio=blend_audio(), user=blend_user())
        self.assertEquals(response.status_code, 403, msg=response.data)

    def test_update_view_no_user(self) -> None:
        """Verify the update view returns a 401 when the user is unauthenticated."""
        response = self.make_update_request(audio=blend_audio())
        self.assertEquals(response.status_code, 401, msg=response.data)

    def test_update_view_change_others_audio(self) -> None:
        """
        Verify the update view returns a 403 when the user has "change_audio" permission but does not own the
        audio.
        """
        response = self.make_update_request(audio=blend_audio(), user=blend_user("Can change audio"))
        self.assertEquals(response.status_code, 403, msg=response.data)

    def test_update_view_change_own_audio(self) -> None:
        """
        Verify the update view returns a 200 when the user has "change_audio" permission and owns the audio.
        """
        user = blend_user("Can change audio")
        audio = blend_audio()
        audio.authors.add(user)
        response = self.make_update_request(audio=audio, user=user)
        self.assertEquals(response.status_code, 200, msg=response.data)

    def make_update_request(self, audio, user=None) -> Response:
        """
        Make a request to the update view and return its response.
        :param audio:      The audio to update.
        :param audio_file: An audio file to attach with the request if any.  Default is None.
        :param user:       The user making the request if any.  Default is None.
        :return:           The Response from the view.
        """
        view = self.view_set.as_view({"put": "update"})
        request = self.request_factory.put("", data=self.data, format="json")
        if user is not None:
            force_authenticate(request, user)
            request.user = user
        return view(request, id=audio.id)

    def test_destroy_view_no_permission(self) -> None:
        """Verify the destroy view returns a 403 when the user is missing permissions."""
        response = self.make_delete_request(audio=blend_audio(), user=blend_user())
        self.assertEquals(response.status_code, 403, msg=response.data)

    def test_destroy_view_no_user(self) -> None:
        """Verify the destroy view returns a 401 when the user is unauthenticated."""
        response = self.make_delete_request(audio=blend_audio())
        self.assertEquals(response.status_code, 401, msg=response.data)

    def test_destroy_view_delete_others_audio(self) -> None:
        """
        Verify the destroy view returns a 403 when the user has "audio_destroy" permission but does not own the
        audio.
        """
        response = self.make_delete_request(audio=blend_audio(), user=blend_user("Can delete audio"))
        self.assertEquals(response.status_code, 403, msg=response.data)

    def test_destroy_view_delete_own_audio(self) -> None:
        """
        Verify the destroy view returns a 204 when the user has "destroy_audio" permission and owns the audio.
        """
        user = blend_user("Can delete audio")
        audio = blend_audio()
        audio.authors.add(user)
        response = self.make_delete_request(audio=audio, user=user)
        self.assertEquals(response.status_code, 204, msg=response.data)

    def make_delete_request(self, audio, user=None) -> Response:
        """
        Make a delete request to the destroy view and return its response.
        :param audio: The audio to delete.
        :param user:  The user making the request if any.  Default is None.
        :return:      The Response from the view.
        """
        view = self.view_set.as_view({"delete": "destroy"})
        request = self.request_factory.delete("")
        if user is not None:
            force_authenticate(request, user)
            request.user = user
        return view(request, id=audio.id)


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
        self.file = TEST_FILE_BYTES
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
        data["file"] = self.file.read()
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

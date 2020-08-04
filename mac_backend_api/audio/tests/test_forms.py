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

import pytest
from django.test import TestCase

from mac_backend_api.audio.forms import AudioCreationForm, AudioUpdateForm


@pytest.mark.django_db
class TestAudioCreationForm(TestCase):
    def test_valid_file(self) -> None:
        """Verify the form is valid when a non-empty file is provided."""
        form = self.get_form()
        self.assertTrue(form.is_valid)

    def test_no_file(self) -> None:
        """Verifies the form is invalid no file is provided."""
        form = self.get_form(file=None)
        self.__assert_file_errors(form)

    def test_empty_file(self) -> None:
        """Verifies the form is invalid when an empty file is provided."""
        form = self.get_form(file=BytesIO())
        self.__assert_file_errors(form)

    def __assert_file_errors(self, form) -> None:
        """Asserts the form is invalid because of the 'file' field."""
        self.assertFalse(form.is_valid())
        self.assertTrue("file" in form.errors)

    def get_form(self, title="Test", description="Test", is_public=True, file=BytesIO(b"content")) -> AudioCreationForm:
        """Returns a filled AudioCreationForm."""
        if isinstance(file, BytesIO):
            file.name = "test_file.mp3"
        return AudioCreationForm({
            "title": title,
            "description": description,
            "is_public": is_public,
            "file": file
        })


@pytest.mark.django_db
class TestAudioUpdateForm(TestCase):
    def setUp(self) -> None:
        pass

    def get_form(self, title="Test", description="Test", is_public=True) -> AudioUpdateForm:
        return AudioUpdateForm({
            "title": title,
            "description": description,
            "is_public": is_public
        })

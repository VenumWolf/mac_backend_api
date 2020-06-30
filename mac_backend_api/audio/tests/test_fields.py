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
from django.test import TestCase
from mixer.backend.django import mixer

from mac_backend_api.audio.fields import is_valid_extension, AudioFormat


@pytest.mark.django_db
class TestAudioFileField(TestCase):
    def test_is_valid_extension(self):
        for extensions in AudioFormat.choices:
            assert is_valid_extension(extensions[0])
        assert not is_valid_extension("not_valid")

    def test_is_valid_extension_uppercase_input(self):
        for extensions in AudioFormat.choices:
            assert is_valid_extension(extensions[0].upper())
        assert not is_valid_extension("NOT_VALID")


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

from mac_backend_api.users.models import User


@pytest.mark.django_db
class TestUserModel(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(User)

    def test_absolute_url(self):
        assert self.user.get_absolute_url() == f"/api/users/{self.user.username}/"

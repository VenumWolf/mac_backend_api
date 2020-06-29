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
from django.test import TestCase, RequestFactory
from mixer.backend.django import mixer

from mac_backend_api.users.api.views import UserViewSet
from mac_backend_api.users.models import User


@pytest.mark.django_db
class TestViewSet(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)
        self.request_factory = RequestFactory()

    def test_get_queryset(self):
        view = UserViewSet()
        request = self.request_factory.get("/fake-url/")
        request.user = self.user
        view.request = request
        assert self.user in view.get_queryset()

    def test_me(self):
        view = UserViewSet()
        request = self.request_factory.get("/fake-url/")
        request.user = self.user
        view.request = request
        response = view.me(request)
        assert response.data == {
            "username": self.user.username,
            "name": self.user.name,
            "is_staff": self.user.is_staff,
            "is_active": self.user.is_active,
            "url": f"http://testserver/api/users/{self.user.username}/",
        }

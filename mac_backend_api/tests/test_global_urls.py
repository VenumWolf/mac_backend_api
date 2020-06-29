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

from django.urls import reverse


class TestAuthUrls:
    def test_token_obtain_url(self):
        assert reverse("token_obtain_pair") == "/api/auth/token/"

    def test_token_refresh_url(self):
        assert reverse("token_refresh") == "/api/auth/token/refresh/"

    def test_token_verify_url(self):
        assert reverse("token_verify") == "/api/auth/token/verify/"

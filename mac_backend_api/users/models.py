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

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from mac_backend_api.utils.random_id.random_id import random_id


class User(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=14,
        default=random_id,
        editable=False)
    name = models.CharField(
        help_text="Name of the user",
        blank=True,
        max_length=255)

    def get_absolute_url(self) -> str:
        return reverse("api:user-detail", kwargs={"username": self.username})


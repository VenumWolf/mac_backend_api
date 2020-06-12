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

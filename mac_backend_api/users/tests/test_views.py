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
            "email": self.user.email,
            "name": self.user.name,
            "url": f"http://testserver/api/users/{self.user.username}/",
        }

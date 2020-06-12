import pytest
from django.urls import resolve, reverse
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestUrls:
    def test_user_detail(self):
        user = mixer.blend("users.User")
        assert reverse("api:user-detail", kwargs={"username": user.username}) == f"/api/users/{user.username}/"
        assert resolve(f"/api/users/{user.username}/").view_name == "api:user-detail"

    def test_user_list(self):
        assert reverse("api:user-list") == "/api/users/"
        assert resolve("/api/users/").view_name == "api:user-list"

    def test_user_me(self):
        assert reverse("api:user-me") == "/api/users/me/"
        assert resolve("/api/users/me/").view_name == "api:user-me"

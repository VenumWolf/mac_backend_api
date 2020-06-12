from uuid import uuid4

import pytest
from mixer.backend.django import mixer

from mac_backend_api.users.forms import UserCreationForm


@pytest.mark.django_db
class TestUserCreationForm:

    def test_new_username(self) -> None:
        form = self.get_form("some_user")
        assert form.is_valid()
        assert form.clean_username() == "some_user"

    def test_existing_username(self) -> None:
        new_user = mixer.blend("users.User")
        form = self.get_form(new_user.username)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors

    def test_mismatched_passwords(self) -> None:
        form = self.get_form("some_user", uuid4(), uuid4())
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors

    def get_form(self, username, password1=None, password2=None) -> UserCreationForm:
        if password1 is None and password2 is None:
            password = uuid4()
            password1 = password
            password2 = password
        return UserCreationForm(
            {
                "username": username,
                "password1": password1,
                "password2": password2,
            }
        )

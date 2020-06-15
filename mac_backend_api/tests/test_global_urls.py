from django.urls import reverse


class TestAuthUrls:
    def test_token_obtain_url(self):
        assert reverse("token_obtain_pair") == "/api/auth/token/"

    def test_token_refresh_url(self):
        assert reverse("token_refresh") == "/api/auth/token/refresh/"

    def test_token_verify_url(self):
        assert reverse("token_verify") == "/api/auth/token/verify/"

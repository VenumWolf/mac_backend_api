from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

from django.urls import reverse


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False)
    name = models.CharField(
        help_text="Name of the user",
        blank=True,
        max_length=255)

    def get_absolute_url(self) -> str:
        return reverse("api:user-detail", kwargs={"username": self.username})


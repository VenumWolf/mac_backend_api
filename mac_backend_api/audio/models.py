from uuid import uuid4

from django.db import models
from django.utils import timezone


class Audio(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        help_text="Unique id of the audio"
    )
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="Title of the audio"
    )
    slug = models.SlugField(
        editable=False,
        null=True,
        blank=True,
        unique=True,
        max_length=200,
        help_text="Url-safe representation of the audio title"
    )
    description = models.TextField(
        max_length=2000,
        blank=True,
        help_text="A short description for the audio"
    )
    listen_count = models.IntegerField(
        default=0,
        editable=False,
        help_text="The number of times the audio has been played"
    )
    uploaded_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="The date and time the audio was uploaded"
    )
    is_public = models.BooleanField(
        default=False,
        help_text="Indicates if the audio should be shown on public indexes, "
                  "it can only be viewed by those with its link"
    )

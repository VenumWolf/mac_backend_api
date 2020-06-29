from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils import timezone

from mac_backend_api.audio.exceptions import UserAlreadyLikesException

User = get_user_model()


class Author(models.Model):
    """
    Provides a layer over the User model.  Audios may be accessed as a queryset through the `audio_set` parameter.
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text="A reference to the User instance"
    )


class Audio(models.Model):
    """
    Provides information storage for an uploaded audio.  The file information is stored on `Stream` objects.
    Audio streams can be accessed as a queryset through the `stream_set` parameter.
    """

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
    authors = models.ManyToManyField(
        to=Author,
        help_text="References to the authors audios"
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

    @property
    def like_count(self) -> int:
        """
        A property referring to the number of people who have liked the audio.

        `like_count` is calculated on-the-fly based on the number of Like objects with audio=self.

        :return: The number of people who have liked the audio
        """
        return Like.objects.filter(audio=self).count()

    def get_absolute_url(self) -> str:
        """
        Resolves a working URL for accessing the Audio over HTTP

        :return: The URL path to the Audio
        """
        return reverse("api:audio-detail", kwargs={"id": self.id})

    def add_listen(self) -> None:
        """
        A convenience method which adds 1 to the `listen_count`.
        """
        self.listen_count += 1
        self.save()

    def add_like(self, user) -> None:
        """
        Add a like to the audio for a given user.

        If the user has already liked the audio, this method will fail silently.

        :param  user: The user liking the audio
        """
        try:
            like = Like(user=user, audio=self)
            like.save()
        except UserAlreadyLikesException:
            pass

    def remove_like(self, user) -> None:
        """
        Remove a like from the audio for a given user.

        If the user has not liked the audio already, this method will fail silently.

        :param user: The user unliking the audio
        """
        try:
            self.like_set.get(user=user, audio=self).delete()
        except ObjectDoesNotExist:
            pass


def get_audio_stream_upload_path(stream, filename) -> str:
    """
    Generates the file path to which an audio stream's file will be stored.
    :param stream:   The audio stream instance
    :param filename: The name of the file (this value is ignored, but is necessary to be used as the upload_to value)
    :return:         The path for the file upload
    """
    return f"audio/{stream.audio.id}/{stream.id}.{stream.format}"


class AudioStream(models.Model):
    class AudioFormat(models.TextChoices):
        MP3 = "mp3"
        AAC = "aac"
        OGG = "ogg"
        WAV = "wav"

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        help_text="The unique ID of the stream"
    )
    audio = models.ForeignKey(
        to=Audio,
        on_delete=models.CASCADE,
        help_text="A reference to the Audio instance"
    )
    format = models.CharField(
        max_length=10,
        choices=AudioFormat.choices,
        help_text="The format of the audio stream"
    )
    bit_rate = models.IntegerField(
        help_text="The stream's bit-rate in hz"
    )
    file = models.FileField(
        upload_to=get_audio_stream_upload_path,
        help_text="The stream's audio file, it will be processed to match the format and bit_rate values"
    )


class Like(models.Model):
    """
    Represents a like (or up-vote.)

    Unlike views, likes must be from a registered user, and each user is allowed to create 1 like per audio.
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text="A reference to the User instance"
    )
    audio = models.ForeignKey(
        to=Audio,
        on_delete=models.CASCADE,
        help_text="A reference to the Audio instance"
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        if self.__is_new_like(self):
            super().save(force_insert, force_update, using, update_fields)
        else:
            raise UserAlreadyLikesException()

    @classmethod
    def __is_new_like(cls, like) -> bool:
        return len(cls.objects.filter(user=like.user, audio=like.audio)) == 0



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

from django.db import models


class AudioFormat(models.TextChoices):
    MP3 = "mp3"
    AAC = "aac"
    OGG = "ogg"
    WAV = "wav"


class AudioBitRate(models.IntegerChoices):
    MINIMAL = 32000
    VERY_LOW = 96000
    LOW = 128000
    AVERAGE = 192000
    HIGH = 256000
    VERY_HIGH = 320000
    MAXIMUM = 512000


class AudioSampleRate(models.IntegerChoices):
    LOW = 44100
    AVERAGE = 48000
    HIGH = 88200
    VERY_HIGH = 96000


def is_valid_extension(extension) -> bool:
    """
    Returns True if a given file extension is a valid audio format.
    :param extension: The file extension to check.
    :return:          True if the file extension is that of a supported audio format.
    """
    return extension.lower() in [extension[0] for extension in AudioFormat.choices]


class AudioFileField(models.FileField):

    def __init__(self, format=AudioFormat.OGG, bit_rate=AudioBitRate.AVERAGE,
                 sample_rate=AudioSampleRate.AVERAGE, **kwargs):
        self.format = format
        self.bit_rate = bit_rate
        self.sample_rate = sample_rate
        super().__init__(**kwargs)


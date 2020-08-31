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

from tempfile import SpooledTemporaryFile

from django.test import TestCase
from pydub import AudioSegment


def get_audio_file(format='mp3', codec=None, bitrate=None, parameters=None, tags=None, id3v2_version='4'):
    audio_data = SpooledTemporaryFile()
    audio_segment = AudioSegment.silent(1000)
    audio_segment.export(audio_data, format, codec, bitrate, parameters, tags, id3v2_version)
    return audio_data


class TestStreamProcessing(TestCase):
    pass



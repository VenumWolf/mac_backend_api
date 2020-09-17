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
from pytest import raises

from mac_backend_api.audio.utils.audio_processing import process_audio, identify_file_format


def get_audio_file(format='mp3', codec=None, bitrate=None, parameters=None, tags=None, id3v2_version='4'):
    audio_data = SpooledTemporaryFile()
    audio_segment = AudioSegment.silent(1000)
    audio_segment.export(audio_data, format, codec, bitrate, parameters, tags, id3v2_version)
    return audio_data


TARGET_FORMATS = ["mp3", "ogg", "wav"]


class TestStreamProcessing(TestCase):
    def test_format_conversion(self):
        """Verifies the file is converted properly for each of the TARGET_FORMATS."""
        for format in TARGET_FORMATS:
            self.assert_converted_to_format(get_audio_file(format="mp3"), format)

    def assert_converted_to_format(self, audio_file, target_format):
        """Runs the file conversion, then asserts that the converted file matches the target format."""
        converted_audio = process_audio(file=audio_file, format=target_format)
        self.assertEquals(identify_file_format(converted_audio), target_format,
                          msg=f"The audio was not converted to the expected format.")


class TestFormatIdentification(TestCase):
    def test_valid_formats(self):
        """Verifies the format identification function can correctly identify required audio formats."""
        audio_files = [(format, get_audio_file(format=format)) for format in TARGET_FORMATS]
        for format, file in audio_files:
            self.assertEquals(identify_file_format(file), format, msg="The file type was not correctly identified.")

    def test_invalid_format(self):
        """Verifies a ValueError is raised if the format identification fun cannot identify a valid audio format."""
        file = SpooledTemporaryFile()
        with raises(ValueError, match="Invalid file format"):
            identify_file_format(file)

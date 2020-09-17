#  Copyright (C) 2020  Mind Audio Central
#
#  This file is part of mac_backend_api.
#
#  mac_backend_api is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  mac_backend_api is distributed in the hope that it will be useful,
#
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with mac_backend_api.  If not, see <https://www.gnu.org/licenses/>.

from tempfile import SpooledTemporaryFile

from filetype import filetype
from pydub import AudioSegment


def default_file_identifier(file) -> str:
    """
    Identifies the file type using the filetype library.
    :param file: A file-like object to identify.
    :return:     A string containing the format name (ex. mp3, ogg, wav, ext.)
    """
    file.seek(0)
    file_type = filetype.guess(file.read())
    if file_type is None:
        raise ValueError("Invalid file format")
    return file_type.extension


def identify_file_format(file, identifier=default_file_identifier) -> str:
    """
    Get the format, or type of data contained within a file.
    :param file:       A file-like object to identify.
    :param identifier: A function which takes a file-like object and returns it's type as a string.  Refer to the
                       specific identification function's documentation for more informatoin.
                       (Default: default_file_identifier())
    :return:           A string containing the format name (ex. mp3, ogg, wav, ext.)
    """
    return identifier(file)


def pydub_audio_processor(file, **kwargs):
    """
    Convert and reformat audio using the Pydub library.
    :param file:   A file, or bytes-like object containing the unprocessed audio data.
    :param kwargs: Parameters passed to Pydub's AudioSegment.export() method (see its documentation for more info.)
    :return:       A file-like object containing the processed audio data.
    """
    output_format = kwargs.get("format")
    file_format = identify_file_format(file)
    file.seek(0)
    audio = AudioSegment.from_file(file, file_format)
    audio.set_frame_rate(kwargs.get("sample_rate", 48000))
    output_file = audio.export(format=output_format)
    output_file.seek(0)
    return output_file


def process_audio(file, processor=pydub_audio_processor, **kwargs):
    """
    Convert and reformat audio using a set converter.
    :param file:      The input file to process.
    :param processor: A function which will process the audio (reference the processor function's
                      documentation for more information.)
    :param kwargs:    The arguments to pass to the processors (reference the processor function's documentation for
                      more information.)
    :return:          A file-like object containing the processed audio data.
    """
    return processor(file, **kwargs)

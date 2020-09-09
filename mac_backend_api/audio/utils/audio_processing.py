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


def default_file_identifier(file) -> str:
    """
    Identifies the file type using the filetype library.
    :param file: A file-like object to identify.
    :return:     A string containing the format name (ex. mp3, ogg, wav, ext.)
    """
    file_type = filetype.guess(file)
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


def process_audio(file, processors=None, **kwargs):
    """
    Convert and reformat audio using a set converter.
    :param file:       The input file to process.
    :param processors: A function or list of functions to apply to the audio (reference the processor function's
                       documentation for more information.)
    :param kwargs:     The arguments to pass to the processors (reference the processor function's documentation for more
                       information.)
    :return:           A file-like object containing the processed audio data.
    """
    return SpooledTemporaryFile()

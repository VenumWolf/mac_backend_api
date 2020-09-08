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

from pydub import AudioSegment


def process_audio(file, processors, *kwargs):
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

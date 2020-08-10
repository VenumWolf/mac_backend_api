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

from rest_framework import serializers

from mac_backend_api.audio.models import Audio, Stream


class StreamSerializer(serializers.ModelSerializer):
    audio = serializers.HyperlinkedRelatedField(
        lookup_field="id",
        required=False,
        queryset=Audio.objects.all(),
        view_name="api:audio-detail"
    )

    file = serializers.FileField(
        required=False,
    )

    class Meta:
        model = Stream
        fields = ["id", "url", "audio", "format", "bit_rate", "sample_rate", "allow_downloads", "file"]

        extra_kwargs = {
            "url": {"view_name": "api:stream-detail", "lookup_field": "id"}
        }


class NestedStreamSerializer(serializers.ModelSerializer):
    """
    This serializer is used primarily by AudioSerializer.  It is the same as StreamSerializer, except it does not
    include a redundant Audio link.
    """
    class Meta:
        model = Stream
        fields = ["id", "url", "format", "bit_rate", "sample_rate", "allow_downloads", "file"]

        extra_kwargs = {
            "url": {"view_name": "api:stream-detail", "lookup_field": "id"}
        }


DEFAULT_STREAM_PRESETS = (
    {
        "format": Stream.AudioFormat.OGG,
        "sample_rate": Stream.AudioSampleRate.HIGH,
        "bit_rate": Stream.AudioBitRate.HIGH
    },
    {
        "format": Stream.AudioFormat.OGG,
        "sample_rate": Stream.AudioSampleRate.AVERAGE,
        "bit_rate": Stream.AudioBitRate.AVERAGE
    },
    {
        "format": Stream.AudioFormat.OGG,
        "sample_rate": Stream.AudioSampleRate.LOW,
        "bit_rate": Stream.AudioBitRate.LOW
    }
)


class AudioSerializer(serializers.ModelSerializer):
    streams = NestedStreamSerializer(
        many=True,
        read_only=True,
    )

    authors = serializers.HyperlinkedRelatedField(
        lookup_field="username",
        many=True,
        read_only=True,
        view_name="api:user-detail"
    )

    file = serializers.FileField(
        required=False,
        help_text=(
            "A file is only required when creating a new Audio for the first time.  Do not provide a file when making "
            "update requests."
        )
    )

    class Meta:
        model = Audio
        fields = ["id", "title", "url", "description", "listen_count", "uploaded_at", "is_public", "authors",
                  "streams", "file"]

        extra_kwargs = {
            "url": {"view_name": "api:audio-detail", "lookup_field": "id"}
        }

    def create(self, validated_data):
        """
        Strips the "file" field, calls
        """
        audio_file = self.pop_file(validated_data)
        audio = super().create(validated_data)
        self.create_default_streams(audio, audio_file)
        return audio

    def pop_file(self, data):
        """
        Pop the file field from the data if it is present.
        :param data: The validated data to pop from
        :return:     The file, or None if the file was not provided.
        """
        if "file" in data.keys():
            file = data.pop("file")
        else:
            file = None
        return file

    def create_default_streams(self, audio, audio_file, presets=DEFAULT_STREAM_PRESETS):
        """
        Create the default streams for the Audio.
        :param audio:      The Audio instance to create
        :param audio_file: A file-like object containing the uploaded audio data.
        :param presets:    A list of dictionaries containing the 'format', 'sample_rate', and 'bit_rate' of the
                           streams to create.  A stream will be created for each entry in the list using the settings
                           provided by the entry.
        """
        for preset in presets:
            stream = Stream(
                audio=audio,
                format=preset.get("format"),
                sample_rate=preset.get("sample_rate"),
                bit_rate=preset.get("bit_rate"),
                file=audio_file
            )
            stream.save()

    def validate(self, data):
        """
        Insert a file check then call the parent validate() method.

        Using this method because validate_file() is only called if the file is not None.
        """
        file = data.get("file", None)
        if self.is_creating_instance() and file is None:
            raise serializers.ValidationError("A file is required when creating new Audio instances")
        if not self.is_creating_instance() and file is not None:
            raise serializers.ValidationError("A file should only be provided when creating new Audio instances")
        return super(AudioSerializer, self).validate(data)

    def is_creating_instance(self) -> bool:
        return self.instance is None

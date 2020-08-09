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
        Removes the file field from the data before attempting to create the Audio instance.
        """
        if "file" in validated_data.keys():
            validated_data.pop("file")
        return super().create(validated_data)

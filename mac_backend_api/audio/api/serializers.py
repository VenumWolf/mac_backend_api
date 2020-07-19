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

from mac_backend_api.audio.models import Audio, AudioStream


class StreamSerializer(serializers.ModelSerializer):
    audio = serializers.HyperlinkedRelatedField(
        lookup_field="id",
        read_only=True,
        view_name="api:audio-detail"
    )

    class Meta:
        model = AudioStream
        fields = ["id", "url", "audio", "format", "bit_rate", "sample_rate", "allow_downloads", "file"]

        extra_kwargs = {
            "url": {"view_name": "api:stream-detail", "lookup_field": "id"}
        }


class AudioSerializer(serializers.ModelSerializer):
    streams = serializers.HyperlinkedRelatedField(
        lookup_field="id",
        many=True,
        read_only=True,
        view_name="api:stream-detail"
    )

    authors = serializers.HyperlinkedRelatedField(
        lookup_field="id",
        many=True,
        read_only=True,
        view_name="api:user-detail"
    )

    class Meta:
        model = Audio
        fields = ["id", "title", "slug", "url", "description", "listen_count", "uploaded_at", "is_public", "authors",
                  "streams"]

        extra_kwargs = {
            "url": {"view_name": "api:audio-detail", "lookup_field": "id"}
        }

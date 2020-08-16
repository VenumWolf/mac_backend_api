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

from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from mac_backend_api.audio.api.serializers import AudioSerializer, StreamSerializer
from mac_backend_api.audio.models import Audio, Stream


class AudioViewSet(ModelViewSet):
    serializer_class = AudioSerializer
    lookup_field = "id"
    queryset = Audio.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def filter_queryset(self, queryset):
        if self.action == "list":
            queryset = queryset.filter(is_public=True)
        return queryset


class StreamViewSet(ModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = "id"
    queryset = Stream.objects.all()

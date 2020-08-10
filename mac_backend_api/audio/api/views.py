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

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from mac_backend_api.audio.api.serializers import AudioSerializer, StreamSerializer
from mac_backend_api.audio.models import Audio, Stream

ERROR_DATA = {
    "file_not_provided": {
            "detail": ErrorDetail("File was not provided"),
            "code": "file_not_provided"
    },

    "file_not_allowed": {
        "detail": ErrorDetail("File upload is not allowed"),
        "code": "file_not_allowed"
    }
}


class AudioViewSet(ModelViewSet):
    serializer_class = AudioSerializer
    lookup_field = "id"
    queryset = Audio.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def filter_queryset(self, queryset):
        if self.action == "list":
            queryset = queryset.filter(is_public=True)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.FILES.get("file") is None:
            response = Response(data=ERROR_DATA.get("file_not_provided"), status=status.HTTP_400_BAD_REQUEST)
        else:
            response = super(AudioViewSet, self).create(request, args, kwargs)
        return response

    def update(self, request, *args, **kwargs):
        if request.FILES.get("file") is not None:
            response = Response(data=ERROR_DATA.get("file_not_allowed"), status=status.HTTP_400_BAD_REQUEST)
        else:
            response = super(AudioViewSet, self).update(request, args, kwargs)
        return response


class StreamViewSet(ModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = "id"
    queryset = Stream.objects.all()

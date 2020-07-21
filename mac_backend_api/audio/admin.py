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
from django.conf import settings
from django.contrib import admin

from mac_backend_api.audio.models import Audio, Stream, Like


class StreamInline(admin.StackedInline):
    model = Stream


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ["title", "uploaded_at", "is_public", "listen_count", "like_count"]
    search_fields = ["title", "authors__username", "streams__format", "streams__bit_rate", "streams__sample_rate"]
    inlines = [StreamInline]


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ["audio__title", "audio__is_public", "audio__uploaded_at", "allow_downloads", "format", "bit_rate",
                    "sample_rate"]
    search_fields = ["audio__title", "audio__authors__username", "format", "bit_rate", "sample_rate"]

    def audio__title(self, instance) -> str:
        return instance.audio.title

    def audio__is_public(self, instance) -> bool:
        return instance.audio.is_public

    def audio__uploaded_at(self, instance) -> str:
        return instance.audio.uploaded_at


@admin.register(Like)
class StreamAdmin(admin.ModelAdmin):
    list_display = ["audio__title", "user"]
    search_fields = ["user__username", "audio__title"]

    def audio__title(self, instance) -> str:
        return instance.audio.title

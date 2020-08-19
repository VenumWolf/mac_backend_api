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

from rest_framework.permissions import BasePermission, SAFE_METHODS

from mac_backend_api.audio.models import Audio, Stream

IS_OWNER_FUNCTIONS = {
    Audio: lambda user, audio: user in audio.authors.all(),
    Stream: lambda user, stream: user in stream.audio.authors.all(),
    "default": lambda user, obj: user == obj.owner,
}


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.method not in SAFE_METHODS:
            model = type(obj)
            function = IS_OWNER_FUNCTIONS.get(model, IS_OWNER_FUNCTIONS.get("default"))
            has_permission = self.is_owner(function, request.user, obj)
        else:
            has_permission = True
        return has_permission

    def is_owner(self, function, user, obj):
        """
        Use the provided function to determine if the user owns the object.
        :param function: The function which determines if a user is the owner of the object.  The function should return
                         a boolean value.
        :param user:     The user making the request.
        :param obj:      The object to check.
        :return:         True if the user owns the object.  If the function raises an Exception, False will always be
                         returned.
        """
        try:
            is_owner = function(user, obj)
        except Exception:
            is_owner = False
        return is_owner

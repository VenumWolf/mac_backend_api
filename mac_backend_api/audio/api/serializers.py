from rest_framework import serializers

from mac_backend_api.audio.models import Audio


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ["id", "title", "slug", "description", "listen_count", "uploaded_at", "is_public", "url"]

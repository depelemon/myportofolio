from django.templatetags.static import static
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Music, Project


def clean_text(value, message):
    value = strip_tags(value).strip()
    if not value:
        raise serializers.ValidationError(message)
    return value


class StarredSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    # Preserve the existing API's privacy policy: publish counts and the current
    # user's status, never the identities of other users who starred an item.
    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(
            request and request.user.is_authenticated
            and any(user.pk == request.user.pk for user in obj.starred_by.all())
        )

    def validate_description(self, value):
        return clean_text(value, "Deskripsi tidak boleh hanya berisi tag HTML.")


class ProjectSerializer(StarredSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "released_at", "thumbnail",
            "star_count", "is_starred",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_text(value, "Judul proyek tidak boleh hanya berisi tag HTML.")


class MusicSerializer(StarredSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = [
            "id", "name", "description", "released_at", "audio_path",
            "audio_url", "star_count", "is_starred",
        ]
        read_only_fields = ["id"]

    def validate_name(self, value):
        return clean_text(value, "Judul lagu tidak boleh hanya berisi tag HTML.")

    def validate_audio_path(self, value):
        return clean_text(value, "Path audio tidak boleh kosong.")

    def get_audio_url(self, obj):
        return static(obj.audio_path)

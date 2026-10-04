from rest_framework import serializers

from .models import Category, Event, Session


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "is_active",
        ]
        read_only_fields = [
            "id",
        ]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            "id",
            "title",
            "description",
            "starts_at",
        ]


class EventStatusField(serializers.Field):

    def to_representation(self, value):
        return "published" if value else "draft"

    def to_internal_value(self, data):
        if data == "published":
            return True

        if data == "draft":
            return False

        raise serializers.ValidationError(
            "Status must be 'published' or 'draft'."
        )


class EventSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(
        many=True,
        read_only=True,
    )

    status = EventStatusField(
        source="is_published",
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "starts_at",
            "capacity",
            "is_published",
            "status",
            "organizer",
            "category",
            "sessions",
        ]

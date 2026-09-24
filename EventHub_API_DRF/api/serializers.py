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


class EventSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Event
        fields = "__all__"

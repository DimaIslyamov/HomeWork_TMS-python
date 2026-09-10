from rest_framework import serializers


class EchoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    topic = serializers.CharField(max_length=100)

    def validate_topic(self, value):
        if value.lower() == "php":
            raise serializers.ValidationError(
                "This topic is not allowed."
            )

        return value

    def validate(self, attrs):
        name = attrs.get("name")
        topic = attrs.get("topic")

        if name.lower() == topic.lower():
            raise serializers.ValidationError(
                "Name and topic must be different."
            )

        return attrs
    
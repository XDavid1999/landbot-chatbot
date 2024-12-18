from dispatcher.models import Topic, Notification, NotificationLog
from rest_framework import serializers
import dataclasses


@dataclasses.dataclass
class TelegramRequirements:
    chat_id: str


@dataclasses.dataclass
class SlackRequirements:
    channel: str


@dataclasses.dataclass
class EmailRequirements:
    recipient_list: list


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

    def validate(self, attrs):
        method = attrs.get("method")
        config = attrs.get("config")

        matches = {
            Notification.TELEGRAM: TelegramRequirements,
            Notification.SLACK: SlackRequirements,
            Notification.EMAIL: EmailRequirements,
        }

        if not isinstance(config, matches[method]):
            raise serializers.ValidationError(f"Invalid config for {method}")

        return attrs


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = "__all__"


class ChatMessageSerializer(serializers.Serializer):
    topic_id = serializers.CharField()
    description = serializers.CharField()

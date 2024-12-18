from dispatcher.models import Topic, Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    method = serializers.ChoiceField(choices=Notification.METHOD_CHOICES)

    class Meta:
        model = Notification
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = Topic
        fields = "__all__"


class ChatMessageSerializer(serializers.Serializer):
    topic_id = serializers.CharField()
    description = serializers.CharField()

from dispatcher.models import Topic, Notification
from rest_framework import viewsets, status
from dispatcher.serializers import (
    TopicSerializer,
    NotificationSerializer,
    ChatMessageSerializer,
)
from rest_framework.response import Response
from dispatcher.tasks.sending import send_notification
import logging

logger = logging.getLogger(__name__)


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Dispatcher(viewsets.ViewSet):
    def post(self, request):
        try:
            serializer = ChatMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            message: str = serializer.validated_data["description"]
            topic_id: int = serializer.validated_data["topic_id"]

            topic = Topic.objects.filter(name=topic_id)
            if not topic.exists():
                return Response(
                    {"message": "No notifications found for this topic"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            send_notification.delay(topic_id=topic_id.id, message=message)

            return Response(
                {"message": "Notifications sent"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Dispatcher error: {e}")
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    """
    ViewSet for handling CRUD operations on Topic instances
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Notification instances
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new Notification instance.

        Args:
            request: The HTTP request object.

        Returns:
            Response: DRF Response object with appropriate status and message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Dispatcher(viewsets.ViewSet):
    """
    ViewSet for handling incoming chat messages and dispatching notifications.
    """

    def post(self, request):
        """
        Handles POST requests to dispatch notifications based on the topic.

        Args:
            request: The HTTP request object.

        Returns:
            Response: DRF Response object with appropriate status and message.
        """
        try:
            serializer = ChatMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            message: str = serializer.validated_data["description"]
            topic_id: int = serializer.validated_data["topic_id"]

            notifications = Notification.objects.filter(topic_id=topic_id)
            if not notifications.exists():
                return Response(
                    {"message": "No notifications found for this topic"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            for notification in notifications:
                send_notification.delay(
                    notification_id=notification.id, message=message
                )

            return Response(
                {"message": "Notifications sent"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Dispatcher error: {e}")
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

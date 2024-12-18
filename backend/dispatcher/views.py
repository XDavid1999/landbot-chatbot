from dispatcher.models import Topic, Notification
from rest_framework import viewsets, status
from dispatcher.serializers import (
    TopicSerializer,
    NotificationSerializer,
    ChatMessageSerializer,
)
from rest_framework.response import Response
from dispatcher.tasks.sending import send_notification


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
            message = serializer.data["description"]

            if notifications := Notification.objects.filter(
                topic=serializer.data["topic_id"]
            ):
                for notification in notifications:
                    send_notification.delay(notification.method, message=message)
            else:
                return Response(
                    {"message": "No notifications found for this topic"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response({"message": "Notification sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

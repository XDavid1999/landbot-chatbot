from dispatcher.models import Topic, Notification, NotificationLog
from rest_framework import viewsets, status
from dispatcher.serializers import (
    TopicSerializer,
    NotificationSerializer,
    NotificationLogSerializer,
    ChatMessageSerializer,
)
from rest_framework.response import Response
from dispatcher.tasks.sending import send_notification
from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailService


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


class NotificationLogViewSet(viewsets.ModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Dispatcher(viewsets.ViewSet):
    def post(self, request):
        try:
            serializer = ChatMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            notification = Notification.objects.exists(
                topic=serializer.data["topic_id"]
            )
            message = serializer.data["description"]
            send_notification.delay(notification.method, message=message)
            NotificationLog.objects.create(
                user=request.user, topic_id=serializer.data["topic_id"], meta=message
            )
            return Response({"message": "Notification sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

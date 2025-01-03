from django.db import models
from backend.utils.django.models.mixins import TimestampedModel
from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailService


class Notification(TimestampedModel):
    EMAIL = "Email"
    SLACK = "Slack"
    TELEGRAM = "Telegram"

    METHOD_CHOICES = [
        (EMAIL, "Email"),
        (SLACK, "Slack"),
        (TELEGRAM, "Telegram"),
    ]

    method = models.CharField(
        max_length=255,
        choices=METHOD_CHOICES,
        # This could control the uniqueness of a method if desired
        unique=False,
    )
    config = models.JSONField()

    def __str__(self):
        return self.method

    def validate(self, instance):
        service = instance.get_service()
        if not service().validate(**instance.config):
            raise ValueError("Invalid notification data")

    def save(self, *args, **kwargs):
        self.validate(self)
        super().save(*args, **kwargs)

    def get_service(self):
        if self.method == Notification.TELEGRAM:
            return TelegramService
        elif self.method == Notification.SLACK:
            return SlackService
        elif self.method == Notification.EMAIL:
            return EmailService
        else:
            raise NotImplementedError


class Topic(TimestampedModel):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="topic",
        null=True,
    )
    # reference to the chatbot token on a secure storage
    chatbot_token = models.CharField(max_length=255, null=True)

    @property
    def secure_storage_token(self):
        # mock the retrieval of the chatbot token
        return self.chatbot_token

    def __str__(self):
        return f"{self.name} - {self.notification}"

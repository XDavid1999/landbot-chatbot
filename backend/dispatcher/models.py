from django.db import models
from backend.utils.django.models.mixins import TimestampedModel
from dispatcher.services.telegram import TelegramService, TelegramRequirements
from dispatcher.services.slack import SlackService, SlackRequirements
from dispatcher.services.email import EmailService, EmailRequirements


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
        return f"{self.method} notification for {self.topic}"

    def validate(self, instance):
        matches = {
            Notification.TELEGRAM: TelegramRequirements,
            Notification.SLACK: SlackRequirements,
            Notification.EMAIL: EmailRequirements,
        }
        matches[instance.method](**instance.config)
        return instance

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

    def __str__(self):
        return self.name

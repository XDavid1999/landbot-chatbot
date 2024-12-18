from django.db import models
from backend.utils.django.models.mixins import TimestampedModel
from dispatcher.services.telegram import TelegramService, TelegramRequirements
from dispatcher.services.slack import SlackService, SlackRequirements
from dispatcher.services.email import EmailService, EmailRequirements


class Topic(TimestampedModel):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()


class Notification(TimestampedModel):
    EMAIL = "Email"
    SLACK = "Slack"
    TELEGRAM = "Telegram"

    METHOD_CHOICES = [
        (EMAIL, "Email"),
        (SLACK, "Slack"),
        (TELEGRAM, "Telegram"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    method = models.CharField(
        max_length=255,
        choices=METHOD_CHOICES,
        # This could control the uniqueness of a method if desired
        unique=False,
    )
    config = models.JSONField()

    def validate(self, attrs):
        method = attrs.get("method")
        config = attrs.get("config")

        matches = {
            Notification.TELEGRAM: TelegramRequirements,
            Notification.SLACK: SlackRequirements,
            Notification.EMAIL: EmailRequirements,
        }

        if not isinstance(config, matches[method]):
            raise ValueError(f"Invalid config for {method}")

        return attrs

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

from django.db import models

from django.contrib.auth.models import User
from backend.utils.django.models.mixins import TimestampedModel


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
    method = models.CharField(max_length=255, choices=METHOD_CHOICES)
    config = models.JSONField()


class NotificationLog(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    meta = models.JSONField()
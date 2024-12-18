from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailService
from dispatcher.models import Notification


class NotificationWrapper(object):
    def __init__(self, notification: Notification, message, *args, **kwargs):
        self.notification = notification
        self.message = message
        self.service = self._get_service(*args, **kwargs)

    def _get_service(self):
        kwargs = self.notification.config
        if self.notification.method == Notification.TELEGRAM:
            kwargs["text"] = self.message
            return TelegramService(**kwargs)
        elif self.notification.method == Notification.SLACK:
            kwargs["text"] = self.message
            return SlackService(**kwargs)
        elif self.notification.method == Notification.EMAIL:
            kwargs["message"] = self.message
            kwargs["subject"] = f"{self.message[:10]}..."
            return EmailService(**kwargs)
        else:
            raise NotImplementedError

    def send(self, *args, **kwargs):
        self.service.send(*args, **kwargs)

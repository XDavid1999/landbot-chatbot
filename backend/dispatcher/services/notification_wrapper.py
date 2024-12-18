from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailService
from dispatcher.models import Notification


class NotificationWrapper(object):
    def __init__(self, notification: Notification, message, *args, **kwargs):
        self.notification = notification
        self.message = message
        service = self.notification.get_service()
        self.client = service(message, **self.notification.config)

    def send(self, *args, **kwargs):
        self.client.send(*args, **kwargs)

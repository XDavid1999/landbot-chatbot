from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailChannel
from dispatcher.models import Notification


class NotificationWrapper(object):
    def __init__(self, type, *args, **kwargs):
        self.type = type
        self.service = self._get_service(type, *args, **kwargs)

    def _get_service(self, type, *args, **kwargs):
        if type == Notification.TELEGRAM:
            return TelegramService(*args, **kwargs)
        elif type == Notification.SLACK:
            return SlackService(*args, **kwargs)
        elif type == Notification.EMAIL:
            return EmailChannel(*args, **kwargs)
        else:
            raise NotImplementedError

    def send(self, *args, **kwargs):
        self.service.send(*args, **kwargs)

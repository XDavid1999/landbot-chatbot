from dispatcher.models import Notification


class NotificationWrapper(object):
    def __init__(self, notification: Notification, message):
        self.notification = notification
        self.message = message
        service = self.notification.get_service()
        self.client = service(message, **self.notification.config)

    def send(self, *args, **kwargs):
        self.client.send(*args, **kwargs)

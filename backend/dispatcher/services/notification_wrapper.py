from dispatcher.models import Notification
from typing import Any


class NotificationWrapper:
    """
    Wrapper for handling the notification sending process.
    """

    def __init__(self, notification: Notification, message: str) -> None:
        """
        Initializes the wrapper with a notification and message.

        Args:
            notification (Notification): The notification instance.
            message (str): The message to send.
        """
        self.notification = notification
        self.message = message
        service_class = self.notification.get_service()
        self.client = service_class(message=self.message, **self.notification.config)

    def send(self, *args: Any, **kwargs: Any) -> None:
        """
        Sends the notification using the appropriate service.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.client.send(*args, **kwargs)

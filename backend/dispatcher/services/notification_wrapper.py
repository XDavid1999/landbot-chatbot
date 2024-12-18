from dispatcher.models import Topic
from typing import Any


class NotificationWrapper:
    """
    Wrapper for handling the topic sending process.
    """

    def __init__(self, topic: Topic, message: str) -> None:
        """
        Initializes the wrapper with a topic and message.

        Args:
            topic (Topic): The topic instance.
            message (str): The message to send.
        """
        self.topic = topic
        self.message = message
        service_class = self.topic.notification.get_service()
        self.client = service_class(**self.topic.config)

    def send(self, *args: Any, **kwargs: Any) -> None:
        """
        Sends the topic using the appropriate service.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.client.send(message=self.message, *args, **kwargs)

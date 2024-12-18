from dispatcher.services.mixins import ServiceInterfaceMixin
from slack_sdk import WebClient
import dataclasses
from typing import Any


@dataclasses.dataclass
class SlackRequirements:
    channel: str


class SlackService(ServiceInterfaceMixin):
    """
    Service for sending notifications via Slack.
    """

    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the Slack service with the necessary configurations.

        Args:
            message (str): The message to send.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, expects 'channel'.
        """
        super().__init__(message, *args, **kwargs)

    def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the Slack WebClient with the API token.
        """
        token: str = self._get_secret("SLACK_API_TOKEN")
        self.client: WebClient = WebClient(token=token)

    def disconnect(self, *args: Any, **kwargs: Any) -> None:
        """
        Closes the Slack WebClient connection if necessary.
        """
        self.client = None

    def validate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Validates that 'channel' is provided.

        Returns:
            bool: True if valid, False otherwise.
        """
        required_fields = ["channel"]
        return all(field in kwargs for field in required_fields)

    def send(self, *args: Any, **kwargs: Any) -> None:
        """
        Sends a message via Slack.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, expects 'channel'.

        Raises:
            ValueError: If validation fails.
            slack_sdk.errors.SlackApiError: If the Slack API call fails.
        """
        if not self.validate(**kwargs):
            raise ValueError("Invalid slack data")

        channel: str = kwargs["channel"]
        self.client.chat_postMessage(text=self.message, channel=channel)

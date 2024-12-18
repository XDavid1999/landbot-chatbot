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

    validator_class = SlackRequirements

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the Slack service with the necessary configurations.

        Args:
            *args: Variable length argument list.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)

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

    def send(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Sends a message via Slack.

        Args:
            message (str): The message to send.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, expects 'channel'.

        Raises:
            ValueError: If validation fails.
            slack_sdk.errors.SlackApiError: If the Slack API call fails.
        """
        if not self.validate(**kwargs):
            raise ValueError("Invalid slack data")

        channel: str = kwargs["channel"]
        self.client.chat_postMessage(text=message, channel=channel)

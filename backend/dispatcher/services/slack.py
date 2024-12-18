from dispatcher.services.mixins import ServiceInterfaceMixin
from slack_sdk import WebClient
import dataclasses


@dataclasses.dataclass
class SlackRequirements:
    channel: str


class SlackService(ServiceInterfaceMixin):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message, **kwargs)

    def connect(self, *args, **kwargs):
        self.client = WebClient(token=self._get_secret("SLACK_API_TOKEN"))

    def disconnect(self, *args, **kwargs):
        self.client = None

    def validate(self, *args, **kwargs):
        required_fields = ["channel"]
        return all([field in kwargs for field in required_fields])

    def send(self, *args, **kwargs):
        if not self.validate(**kwargs):
            raise ValueError("Invalid slack data")
        self.client.chat_postMessage(text=self.message, **kwargs)

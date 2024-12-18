from dispatcher.services.mixins import ServiceInterfaceMixin
from slack_sdk import WebClient


class SlackService(ServiceInterfaceMixin):
    def __init__(self, *args, **kwargs):
        pass

    def connect(self, *args, **kwargs):
        self.client = WebClient(token=self._get_secret("SLACK_API_TOKEN"))

    def disconnect(self, *args, **kwargs):
        self.client = None

    def validate(self, *args, **kwargs):
        required_fields = ["text", "channel"]
        return all([field in kwargs for field in required_fields])

    def send(self, *args, **kwargs):
        if not self.validate():
            raise ValueError("Invalid slack data")
        self.client.chat_postMessage(**kwargs)

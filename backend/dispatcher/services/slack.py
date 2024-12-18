from backend.dispatcher.services.mixins import ServiceInterfaceMixin
from slack_sdk import WebClient


class SlackService(ServiceInterfaceMixin):
    def __init__(self, *args, **kwargs):
        pass

    def connect(self, *args, **kwargs):
        self.client = WebClient(token=self._get_secret("SLACK_API_TOKEN"))

    def disconnect(self, *args, **kwargs):
        self.client = None

    def send(self, *args, **kwargs):
        self.client.chat_postMessage(**kwargs)

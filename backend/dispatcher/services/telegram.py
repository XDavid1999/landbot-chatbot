from dispatcher.services.mixins import ServiceInterfaceMixin
import requests


class TelegramService(ServiceInterfaceMixin):
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, *args, **kwargs):
        self.bot_token = self._get_secret("TELEGRAM_BOT_TOKEN")
        self.chat_id = kwargs.get("chat_id")

    def connect(self, *args, **kwargs):
        pass

    def disconnect(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        url = f"{self.BASE_URL}{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": kwargs.get("text")}
        requests.post(url, data=data)

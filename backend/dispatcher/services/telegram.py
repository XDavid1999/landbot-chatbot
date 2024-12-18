from dispatcher.services.mixins import ServiceInterfaceMixin
import requests
import dataclasses


@dataclasses.dataclass
class TelegramRequirements:
    chat_id: str


class TelegramService(ServiceInterfaceMixin):
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, message, *args, **kwargs):
        self.bot_token = self._get_secret("TELEGRAM_BOT_TOKEN")
        self.chat_id = kwargs.get("chat_id")
        super().__init__(message, **kwargs)

    def connect(self, *args, **kwargs):
        pass

    def disconnect(self, *args, **kwargs):
        pass

    def validate(self, *args, **kwargs):
        required_fields = ["chat_id"]
        return all([field in kwargs for field in required_fields])

    def send(self, *args, **kwargs):
        if not self.validate(**kwargs):
            raise ValueError("Invalid telegram data")

        url = f"{self.BASE_URL}{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": self.message}
        requests.post(url, data=data)

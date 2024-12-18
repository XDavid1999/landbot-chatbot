from rest_framework import status
from dispatcher.services.mixins import ServiceInterfaceMixin
import requests
import dataclasses
from typing import Any, Dict


@dataclasses.dataclass
class TelegramRequirements:
    chat_id: str


class TelegramService(ServiceInterfaceMixin):
    """
    Service for sending notifications via Telegram.
    """

    validator_class = TelegramRequirements
    BASE_URL: str = "https://api.telegram.org/bot"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the Telegram service with the necessary configurations.

        Args:
            *args: Variable length argument list.
            **kwargs: Additional keyword arguments.
        """
        self.bot_token: str = self._get_secret("TELEGRAM_BOT_TOKEN")
        super().__init__(*args, **kwargs)

    def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Telegram does not require an explicit connection.
        """
        pass

    def disconnect(self, *args: Any, **kwargs: Any) -> None:
        """
        Telegram does not require an explicit disconnection.
        """
        pass

    def send(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Sends a message via Telegram.

        Args:
            message (str): The message to send.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValueError: If validation fails.
            requests.RequestException: If the HTTP request fails.
        """
        if not self.validate(**kwargs):
            raise ValueError("Invalid telegram data")

        url: str = f"{self.BASE_URL}{self.bot_token}/sendMessage"
        data: Dict[str, str] = {"chat_id": kwargs.get("chat_id"), "text": message}
        response = requests.post(url, data=data)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise ValueError(
                "Invalid chat_id. Have you started a conversation with the bot?"
            )

        response.raise_for_status()

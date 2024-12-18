from django.core import mail
from dispatcher.services.mixins import ServiceInterfaceMixin
import dataclasses
from typing import Any, List


@dataclasses.dataclass
class EmailRequirements:
    recipient_list: list


class EmailService(ServiceInterfaceMixin):
    """
    Service for sending notifications via Email.
    """

    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the Email service with the necessary configurations.

        Args:
            message (str): The message to send.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, expects 'recipient_list' and optionally 'subject'.
        """
        super().__init__(message, *args, **kwargs)

    def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Email service does not require an explicit connection.
        """
        pass

    def disconnect(self, *args: Any, **kwargs: Any) -> None:
        """
        Email service does not require an explicit disconnection.
        """
        pass

    def validate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Validates that 'recipient_list' is provided and is a list.

        Returns:
            bool: True if valid, False otherwise.
        """
        required_fields = ["recipient_list"]
        if not all(field in kwargs for field in required_fields):
            return False
        if not isinstance(kwargs["recipient_list"], list):
            return False
        return True

    def send(self, *args: Any, **kwargs: Any) -> None:
        """
        Sends an email.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, expects 'recipient_list' and optionally 'subject'.

        Raises:
            ValueError: If validation fails.
        """
        if not self.validate(**kwargs):
            raise ValueError("Invalid email data")

        recipient_list: List[str] = kwargs["recipient_list"]
        subject: str = kwargs.get("subject", f"Notification: {self.message[:10]}...")
        mail.send_mail(
            subject=subject,
            message=self.message,
            from_email=None,  # Use default from settings
            recipient_list=recipient_list,
            fail_silently=False,
        )

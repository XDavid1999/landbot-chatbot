from django.core import mail
from dispatcher.services.mixins import ServiceInterfaceMixin
import dataclasses
from typing import Any, List, Optional
from django.core.validators import validate_email


@dataclasses.dataclass
class EmailRequirements:
    recipient_list: list
    subject: Optional[str] = None

    def __post_init__(self):
        for recipient in self.recipient_list:
            validate_email(recipient)


class EmailService(ServiceInterfaceMixin):
    """
    Service for sending notifications via Email.
    """

    validator_class = EmailRequirements

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the Email service with the necessary configurations.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, expects 'recipient_list' and optionally 'subject'.
        """
        super().__init__(*args, **kwargs)

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

    def send(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Sends an email.

        Args:
            message (str): The message to send.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, expects 'recipient_list' and optionally 'subject'.

        Raises:
            ValueError: If validation fails.
        """
        if not self.validate(**kwargs):
            raise ValueError("Invalid email data")

        recipient_list: List[str] = kwargs["recipient_list"]
        subject: str = kwargs.get("subject", f"Notification: {message[:10]}...")
        mail.send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Use default from settings
            recipient_list=recipient_list,
            fail_silently=False,
        )

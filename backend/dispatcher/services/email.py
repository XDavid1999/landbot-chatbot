from django.core import mail
from dispatcher.services.mixins import ServiceInterfaceMixin
import dataclasses


@dataclasses.dataclass
class EmailRequirements:
    recipient_list: list


class EmailService(ServiceInterfaceMixin):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)

    def connect(self, **kwargs):
        pass

    def disconnect(self, **kwargs):
        pass

    def validate(self, **kwargs):
        required_fields = ["recipient_list"]
        return all([field in kwargs for field in required_fields])

    def send(self, **kwargs):
        if not self.validate(**kwargs):
            raise ValueError("Invalid email data")
        subject = kwargs.get("subject", f"{self.message[:10]}...")
        mail.send_mail(message=self.message, subject=subject, **kwargs)

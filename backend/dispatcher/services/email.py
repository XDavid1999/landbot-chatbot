from django.core.mail import send_mail
from dispatcher.services.mixins import ServiceInterfaceMixin


class EmailService(ServiceInterfaceMixin):

    def __init__(self, **kwargs):
        pass

    def connect(self, **kwargs):
        pass

    def disconnect(self, **kwargs):
        pass

    def validate(self, **kwargs):
        required_fields = ["subject", "message", "from_email", "recipient_list"]
        return all([field in kwargs for field in required_fields])

    def send(self, **kwargs):
        if not self.validate(**kwargs):
            raise ValueError("Invalid email data")
        send_mail(**kwargs)

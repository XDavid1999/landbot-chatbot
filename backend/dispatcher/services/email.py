from django.core.mail import send_mail
from backend.dispatcher.services.mixins import ServiceInterfaceMixin


class EmailChannel(ServiceInterfaceMixin):

    def __init__(self, *args, **kwargs):
        pass

    def connect(self, *args, **kwargs):
        pass

    def disconnect(self, *args, **kwargs):
        pass

    def send(self, **kwargs):
        send_mail(**kwargs)

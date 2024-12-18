import unittest
from unittest.mock import patch, MagicMock
from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailService
from dispatcher.services.mixins import ServiceInterfaceMixin


class TestServiceInterfaceMixin(unittest.TestCase):
    """
    Test cases for ServiceInterfaceMixin.
    """

    class ConcreteService(ServiceInterfaceMixin):
        """
        Concrete implementation for testing purposes.
        """

        def send(self, *args, **kwargs):
            pass

        def connect(self, *args, **kwargs):
            pass

        def disconnect(self, *args, **kwargs):
            pass

    def test_initialization(self):
        service = self.ConcreteService(message="Test Message")
        self.assertEqual(service.message, "Test Message")

    def test_get_secret_success(self):
        with patch.dict("os.environ", {"TEST_SECRET": "secret_value"}):
            service = self.ConcreteService(message="Test")
            secret = service._get_secret("TEST_SECRET")
            self.assertEqual(secret, "secret_value")

    def test_get_secret_missing(self):
        service = self.ConcreteService(message="Test")
        with self.assertRaises(KeyError):
            service._get_secret("MISSING_SECRET")

    def test_context_manager(self):
        service = self.ConcreteService(message="Test")
        with patch.object(service, "connect") as mock_connect, patch.object(
            service, "disconnect"
        ) as mock_disconnect:
            with service:
                mock_connect.assert_called_once()
            mock_disconnect.assert_called_once()

    def test_validate_default(self):
        service = self.ConcreteService(message="Test")
        self.assertTrue(service.validate())


class TestTelegramService(unittest.TestCase):
    """
    Test cases for TelegramService.
    """

    @patch("dispatcher.services.telegram.os.getenv")
    @patch("dispatcher.services.telegram.requests.post")
    def test_send_success(self, mock_post, mock_getenv):
        mock_getenv.return_value = "dummy_token"
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        service = TelegramService(message="Hello Telegram!", chat_id="123456")
        service.send(chat_id="123456")

        mock_post.assert_called_once_with(
            "https://api.telegram.org/botdummy_token/sendMessage",
            data={"chat_id": "123456", "text": "Hello Telegram!"},
        )

    @patch("dispatcher.services.telegram.os.getenv")
    def test_validate_success(self, mock_getenv):
        service = TelegramService(message="Hello Telegram!", chat_id="123456")
        self.assertTrue(service.validate(chat_id="123456"))

    def test_validate_failure(self):
        service = TelegramService(message="Hello Telegram!", chat_id="")
        self.assertFalse(service.validate())

    @patch("dispatcher.services.telegram.os.getenv", return_value="dummy_token")
    def test_init(self, mock_getenv):
        service = TelegramService(message="Hello Telegram!", chat_id="123456")
        self.assertEqual(service.bot_token, "dummy_token")
        self.assertEqual(service.chat_id, "123456")


class TestSlackService(unittest.TestCase):
    """
    Test cases for SlackService.
    """

    @patch("dispatcher.services.slack.os.getenv")
    @patch("dispatcher.services.slack.WebClient")
    def test_send_success(self, mock_webclient, mock_getenv):
        mock_getenv.return_value = "dummy_slack_token"
        mock_client_instance = MagicMock()
        mock_webclient.return_value = mock_client_instance

        service = SlackService(message="Hello Slack!", channel="#general")
        service.connect()
        service.send(channel="#general")

        mock_webclient.assert_called_once_with(token="dummy_slack_token")
        mock_client_instance.chat_postMessage.assert_called_once_with(
            text="Hello Slack!", channel="#general"
        )

    @patch("dispatcher.services.slack.os.getenv")
    def test_validate_success(self, mock_getenv):
        service = SlackService(message="Hello Slack!", channel="#general")
        self.assertTrue(service.validate(channel="#general"))

    def test_validate_failure(self):
        service = SlackService(message="Hello Slack!", channel="")
        self.assertFalse(service.validate())

    @patch("dispatcher.services.slack.os.getenv", return_value="dummy_slack_token")
    def test_init(self, mock_getenv):
        service = SlackService(message="Hello Slack!", channel="#general")
        self.assertEqual(service.message, "Hello Slack!")
        self.assertEqual(service.chat_id, "")  # SlackService does not have chat_id


class TestEmailService(unittest.TestCase):
    """
    Test cases for EmailService.
    """

    @patch("dispatcher.services.email.mail.send_mail")
    def test_send_success_with_subject(self, mock_send_mail):
        service = EmailService(
            message="Hello Email!",
            recipient_list=["test@example.com"],
            subject="Greetings",
        )
        service.send(recipient_list=["test@example.com"], subject="Greetings")
        mock_send_mail.assert_called_once_with(
            subject="Greetings",
            message="Hello Email!",
            from_email=None,
            recipient_list=["test@example.com"],
            fail_silently=False,
        )

    @patch("dispatcher.services.email.mail.send_mail")
    def test_send_success_without_subject(self, mock_send_mail):
        service = EmailService(
            message="Hello Email!", recipient_list=["test@example.com"]
        )
        service.send(recipient_list=["test@example.com"])
        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(kwargs["subject"], "Notification: Hello Ema...")

    def test_validate_success(self):
        service = EmailService(
            message="Hello Email!", recipient_list=["test@example.com"]
        )
        self.assertTrue(service.validate(recipient_list=["test@example.com"]))

    def test_validate_failure_missing_field(self):
        service = EmailService(message="Hello Email!", recipient_list=[])
        self.assertFalse(service.validate())

    def test_validate_failure_wrong_type(self):
        service = EmailService(message="Hello Email!", recipient_list="not_a_list")
        self.assertFalse(service.validate())

    def test_init(self):
        service = EmailService(
            message="Hello Email!", recipient_list=["test@example.com"]
        )
        self.assertEqual(service.message, "Hello Email!")
        self.assertEqual(service.chat_id, "")  # EmailService does not have chat_id


if __name__ == "__main__":
    unittest.main()

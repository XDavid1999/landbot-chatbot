# dispatcher/tests/test_services.py

from django.test import TestCase
from unittest.mock import patch, MagicMock
from dispatcher.models import Notification, Topic
from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailService
from dispatcher.services.notification_wrapper import NotificationWrapper
from django.core import mail
from django.core.exceptions import ValidationError
import os


class TelegramServiceTest(TestCase):
    def setUp(self):
        self.telegram_config = {"chat_id": "123456789"}

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "dummy_telegram_token"})
    @patch("dispatcher.services.telegram.requests.post")
    def test_send_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        service = TelegramService(**self.telegram_config)
        try:
            service.send(message="Hello Telegram!", **self.telegram_config)
        except Exception as e:
            self.fail(f"TelegramService.send() raised an exception: {e}")

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        expected_url = "https://api.telegram.org/botdummy_telegram_token/sendMessage"
        self.assertIn(expected_url, args)
        self.assertEqual(
            kwargs["data"], {"chat_id": "123456789", "text": "Hello Telegram!"}
        )

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "dummy_telegram_token"})
    @patch("dispatcher.services.telegram.requests.post")
    def test_send_invalid_chat_id(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        service = TelegramService(chat_id="invalid_chat_id")
        with self.assertRaises(ValueError) as context:
            service.send(message="Hello Telegram!", chat_id="invalid_chat_id")
        self.assertIn("Invalid chat_id", str(context.exception))


class SlackServiceTest(TestCase):
    def setUp(self):
        self.slack_config = {"channel": "#general"}

    @patch.dict(os.environ, {"SLACK_API_TOKEN": "dummy_slack_token"})
    @patch("dispatcher.services.slack.WebClient.chat_postMessage")
    @patch("dispatcher.services.slack.WebClient.__init__", return_value=None)
    def test_send_success(self, mock_init, mock_chat_post):
        mock_chat_post.return_value = MagicMock()

        service = SlackService(**self.slack_config)
        try:
            service.send(message="Hello Slack!", **self.slack_config)
        except Exception as e:
            self.fail(f"SlackService.send() raised an exception: {e}")

        mock_chat_post.assert_called_once_with(text="Hello Slack!", channel="#general")

    @patch.dict(os.environ, {"SLACK_API_TOKEN": "dummy_slack_token"})
    @patch(
        "dispatcher.services.slack.WebClient.chat_postMessage",
        side_effect=Exception("Slack API Error"),
    )
    @patch("dispatcher.services.slack.WebClient.__init__", return_value=None)
    def test_send_failure(self, mock_init, mock_chat_post):
        service = SlackService(**self.slack_config)
        with self.assertRaises(Exception) as context:
            service.send(message="Hello Slack!", **self.slack_config)
        self.assertIn("Slack API Error", str(context.exception))


class EmailServiceTest(TestCase):
    def setUp(self):
        self.email_config = {
            "recipient_list": ["test@example.com"],
            "subject": "Test Subject",
        }
        self.service = EmailService(**self.email_config)

    @patch("dispatcher.services.email.mail.send_mail")
    def test_send_success(self, mock_send_mail):
        self.service.send(message="Hello Email!", **self.email_config)
        mock_send_mail.assert_called_once_with(
            subject="Test Subject",
            message="Hello Email!",
            from_email=None,
            recipient_list=["test@example.com"],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 0)  # Since send_mail is mocked

    @patch("dispatcher.services.email.mail.send_mail")
    def test_send_invalid_email(self, mock_send_mail):
        invalid_config = {"recipient_list": ["invalid-email"], "subject": "Test Email"}
        with self.assertRaises(ValidationError):
            service = EmailService(**invalid_config)
            service.send(message="This should fail", **invalid_config)

    @patch("dispatcher.services.email.mail.send_mail")
    def test_send_without_subject(self, mock_send_mail):
        config = {"recipient_list": ["test@example.com"]}
        service = EmailService(**config)
        service.send(message="Hello without subject!", **config)
        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        expected_subject = "Notification: Hello with..."
        self.assertEqual(kwargs["subject"], expected_subject)
        self.assertEqual(kwargs["message"], "Hello without subject!")


class NotificationWrapperTest(TestCase):
    @patch.dict(
        os.environ,
        {
            "TELEGRAM_BOT_TOKEN": "dummy_telegram_token",
            "SLACK_API_TOKEN": "dummy_slack_token",
        },
    )
    @patch("dispatcher.services.email.mail.send_mail")
    @patch("dispatcher.services.telegram.requests.post")
    @patch("dispatcher.services.slack.WebClient.chat_postMessage")
    @patch("dispatcher.services.slack.WebClient.__init__", return_value=None)
    def test_wrapper_send_email(
        self, mock_slack_init, mock_slack_post, mock_telegram_post, mock_send_mail
    ):
        # Setup
        email_config = {
            "recipient_list": ["test@example.com"],
            "subject": "Wrapper Test Email",
        }
        notification = Notification.objects.create(
            method=Notification.EMAIL, config=email_config
        )
        topic = Topic.objects.create(
            name="Wrapper Topic",
            description="Testing NotificationWrapper",
            notification=notification,
        )
        wrapper = NotificationWrapper(topic=topic)

        # Action
        wrapper.send(message="Hello from Wrapper!")

        # Assertions
        mock_send_mail.assert_called_once_with(
            subject="Wrapper Test Email",
            message="Hello from Wrapper!",
            from_email=None,
            recipient_list=["test@example.com"],
            fail_silently=False,
        )

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "dummy_telegram_token"})
    @patch("dispatcher.services.telegram.requests.post")
    def test_wrapper_send_telegram(self, mock_post):
        # Setup
        telegram_config = {"chat_id": "987654321"}
        notification = Notification.objects.create(
            method=Notification.TELEGRAM, config=telegram_config
        )
        topic = Topic.objects.create(
            name="Wrapper Topic",
            description="Testing NotificationWrapper",
            notification=notification,
        )
        wrapper = NotificationWrapper(topic=topic)

        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Action
        wrapper.send(message="Hello Telegram via Wrapper!")

        # Assertions
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        expected_url = "https://api.telegram.org/botdummy_telegram_token/sendMessage"
        self.assertIn(expected_url, args)
        self.assertEqual(
            kwargs["data"],
            {"chat_id": "987654321", "text": "Hello Telegram via Wrapper!"},
        )

    @patch.dict(os.environ, {"SLACK_API_TOKEN": "dummy_slack_token"})
    @patch("dispatcher.services.slack.WebClient.chat_postMessage")
    @patch("dispatcher.services.slack.WebClient.__init__", return_value=None)
    def test_wrapper_send_slack(self, mock_init, mock_chat_post):
        # Setup
        slack_config = {"channel": "#alerts"}
        notification = Notification.objects.create(
            method=Notification.SLACK, config=slack_config
        )
        topic = Topic.objects.create(
            name="Wrapper Topic",
            description="Testing NotificationWrapper",
            notification=notification,
        )
        wrapper = NotificationWrapper(topic=topic)

        # Action
        wrapper.send(message="Hello Slack via Wrapper!")

        # Assertions
        mock_chat_post.assert_called_once_with(
            text="Hello Slack via Wrapper!", channel="#alerts"
        )

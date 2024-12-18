from django.test import TestCase
from dispatcher.models import Notification, Topic


class NotificationModelTest(TestCase):
    def setUp(self):
        self.telegram_config = {"chat_id": "123456789"}
        self.slack_config = {"channel": "#general"}
        self.email_config = {
            "recipient_list": ["test@example.com"],
            "subject": "Test Subject",
        }

    def test_create_notification_email(self):
        notification = Notification.objects.create(
            method=Notification.EMAIL, config=self.email_config
        )
        self.assertEqual(notification.method, Notification.EMAIL)
        self.assertEqual(notification.config, self.email_config)

    def test_create_notification_slack(self):
        notification = Notification.objects.create(
            method=Notification.SLACK, config=self.slack_config
        )
        self.assertEqual(notification.method, Notification.SLACK)
        self.assertEqual(notification.config, self.slack_config)

    def test_create_notification_telegram(self):
        notification = Notification.objects.create(
            method=Notification.TELEGRAM, config=self.telegram_config
        )
        self.assertEqual(notification.method, Notification.TELEGRAM)
        self.assertEqual(notification.config, self.telegram_config)

    def test_invalid_notification_method(self):
        with self.assertRaises(NotImplementedError):
            Notification.objects.create(method="InvalidMethod", config={})

    def test_notification_validation_on_save(self):
        # Assuming TelegramService.validate will be mocked in service tests
        # Here we ensure that saving a valid notification does not raise errors
        notification = Notification(method=Notification.EMAIL, config=self.email_config)
        try:
            notification.save()
        except ValueError:
            self.fail("Notification.save() raised ValueError unexpectedly!")

    def test_str_method(self):
        notification = Notification(method=Notification.EMAIL, config=self.email_config)
        self.assertEqual(str(notification), Notification.EMAIL)


class TopicModelTest(TestCase):
    def setUp(self):
        self.email_config = {
            "recipient_list": ["test@example.com"],
            "subject": "Test Subject",
        }
        self.notification = Notification.objects.create(
            method=Notification.EMAIL, config=self.email_config
        )

    def test_create_topic(self):
        topic = Topic.objects.create(
            name="Test Topic",
            description="A description for test topic",
            notification=self.notification,
        )
        self.assertEqual(topic.name, "Test Topic")
        self.assertEqual(topic.description, "A description for test topic")
        self.assertEqual(topic.notification, self.notification)

    def test_unique_topic_name(self):
        Topic.objects.create(
            name="Unique Topic",
            description="First instance",
            notification=self.notification,
        )
        with self.assertRaises(Exception):
            # Depending on the database, this might raise IntegrityError or similar
            Topic.objects.create(
                name="Unique Topic",
                description="Second instance",
                notification=self.notification,
            )

    def test_topic_str_method(self):
        topic = Topic(
            name="Sample Topic",
            description="Sample Description",
            notification=self.notification,
        )
        expected_str = f"{topic.name} - {topic.notification}"
        self.assertEqual(str(topic), expected_str)

import pytest
from dispatcher.models import Notification, Topic
from dispatcher.services.telegram import TelegramService
from dispatcher.services.slack import SlackService
from dispatcher.services.email import EmailService


@pytest.fixture
def topic():
    return Topic.objects.create(name="Test Topic", description="A test topic.")


@pytest.mark.django_db
def test_notification_creation_valid_telegram(topic):
    config = {"chat_id": "12345"}
    notification = Notification.objects.create(
        topic=topic, method=Notification.TELEGRAM, config=config
    )

    assert notification.method == Notification.TELEGRAM
    assert notification.config == config
    assert notification.get_service() == TelegramService


@pytest.mark.django_db
def test_notification_creation_valid_slack(topic):
    config = {"channel": "general"}
    notification = Notification.objects.create(
        topic=topic, method=Notification.SLACK, config=config
    )

    assert notification.method == Notification.SLACK
    assert notification.config == config
    assert notification.get_service() == SlackService


@pytest.mark.django_db
def test_notification_creation_valid_email(topic):
    config = {"recipient_list": ["test@example.com"]}
    notification = Notification.objects.create(
        topic=topic, method=Notification.EMAIL, config=config
    )

    assert notification.method == Notification.EMAIL
    assert notification.config == config
    assert notification.get_service() == EmailService


@pytest.mark.django_db
def test_notification_creation_invalid_config(topic):
    invalid_config = {"invalid_key": "value"}

    with pytest.raises(ValueError, match="Invalid config for Telegram"):
        Notification.objects.create(
            topic=topic, method=Notification.TELEGRAM, config=invalid_config
        )


@pytest.mark.django_db
def test_notification_get_service_invalid_method(topic):
    notification = Notification.objects.create(
        topic=topic, method="InvalidMethod", config={}
    )

    with pytest.raises(NotImplementedError):
        notification.get_service()

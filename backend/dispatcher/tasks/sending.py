from celery import shared_task
from dispatcher.services.notification_wrapper import NotificationWrapper
from dispatcher.models import Topic
import logging
from typing import Any
from dispatcher.settings import NOTIFICATION_RETY_TIME

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task(bind=True)
def send_notification(self, pk: str, message: str, **kwargs: Any) -> None:
    """
    Celery task to send notifications asynchronously.

    Args:
        pk (int): The ID of the Topic instance.
        message (str): The message to send.
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If any error occurs during the sending process.
    """
    logger.info(f"Sending topic ID {pk}")
    topic = Topic.objects.get(id=pk)

    if not hasattr(topic, "notification"):
        logger.info("This topic has not any notification method, skipping")
    else:
        try:
            logger.info(f"Topic method: {topic.notification.method}")
            notification_wrapper = NotificationWrapper(topic)
            notification_wrapper.send(message, **kwargs)
            logger.info(f"Topic ID {pk} sent successfully.")
        except Topic.DoesNotExist:
            logger.error(f"Topic with ID {pk} not found.")
        except Exception as e:
            logger.error(f"Error sending topic ID {pk}: {e}")
            raise self.retry(exc=e, countdown=NOTIFICATION_RETY_TIME)

from celery import shared_task
from dispatcher.services.notification_wrapper import NotificationWrapper
from dispatcher.models import Topic
import logging
from typing import Any

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_notification(self, topic_id: int, message: str, **kwargs: Any) -> None:
    """
    Celery task to send notifications asynchronously.

    Args:
        topic_id (int): The ID of the Topic instance.
        message (str): The message to send.
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If any error occurs during the sending process.
    """
    logger.info(f"Sending topic ID {topic_id}")
    topic = Topic.objects.get(id=topic_id)

    if not hasattr(topic, "notification"):
        logger.info("This topic has not any notification method, skipping")
    else:
        try:
            logger.info(f"Topic method: {topic.notification.method}")
            notification_wrapper = NotificationWrapper(topic, message)
            notification_wrapper.send(**kwargs)
            logger.info(f"Topic ID {topic_id} sent successfully.")
        except Topic.DoesNotExist:
            logger.error(f"Topic with ID {topic_id} not found.")
        except Exception as e:
            logger.error(f"Error sending topic ID {topic_id}: {e}")
        raise self.retry(exc=e, countdown=60)

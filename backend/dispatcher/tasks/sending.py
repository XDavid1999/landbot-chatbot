from celery import shared_task
from dispatcher.services.notification_wrapper import NotificationWrapper
from dispatcher.models import Notification
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_notification(self, notification_id: int, message: str, **kwargs: Any) -> None:
    """
    Celery task to send notifications asynchronously.

    Args:
        notification_id (int): The ID of the Notification instance.
        message (str): The message to send.
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If any error occurs during the sending process.
    """
    try:
        logger.info(f"Sending notification ID {notification_id}")
        notification = Notification.objects.get(id=notification_id)
        logger.info(f"Notification method: {notification.method}")
        notification_wrapper = NotificationWrapper(notification, message)
        notification_wrapper.send(**kwargs)
        logger.info(f"Notification ID {notification_id} sent successfully.")
    except Notification.DoesNotExist:
        logger.error(f"Notification with ID {notification_id} not found.")
    except Exception as e:
        logger.error(f"Error sending notification ID {notification_id}: {e}")
        raise self.retry(exc=e, countdown=60)  # Retry after 60 seconds

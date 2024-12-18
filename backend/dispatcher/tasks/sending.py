from celery import shared_task
from backend.dispatcher.services.notification_wrapper import NotificationWrapper
from backend.dispatcher.models import Notification
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_notification(topic, **kwargs):
    try:
        logger.info(f"Sending notification for topic {topic}")
        notification = Notification.objects.get(topic=topic)
        logger.info(f"Notification method: {notification.method}")
        notification_wrapper = NotificationWrapper(notification.method)
        notification_wrapper.send(**kwargs)
    except Notification.DoesNotExist:
        logger.error(f"Notification for topic {topic} not found")
    except Exception as e:
        logger.error(f"Error sending notification for topic {topic}: {e}")

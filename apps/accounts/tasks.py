from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_id):
    """
    Background task to send a welcome email to newly registered users.
    """
    logger.info(f"Sending welcome email to user_id: {user_id}")
    # TODO: Implement email sending logic
    return True

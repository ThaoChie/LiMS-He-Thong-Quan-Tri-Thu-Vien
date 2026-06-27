from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_borrow_confirmation_email(borrow_id):
    """
    Background task to send a borrow confirmation email.
    """
    logger.info(f"Sending borrow confirmation email for borrow_id: {borrow_id}")
    # TODO: Implement email sending logic
    return True

@shared_task
def send_reservation_available_email(reservation_id):
    """
    Background task to send an email when a reserved book becomes available.
    """
    logger.info(f"Sending reservation available email for reservation_id: {reservation_id}")
    # TODO: Implement email sending logic
    return True

@shared_task
def remind_due_date_task():
    """
    Cronjob task to remind users of upcoming due dates.
    """
    logger.info("Running remind due date task")
    # TODO: Implement reminder logic
    return True

@shared_task
def auto_expire_reservations():
    """
    Cronjob task to auto expire reservations that have exceeded their hold period.
    """
    logger.info("Running auto expire reservations task")
    # TODO: Implement auto expire logic
    return True

@shared_task
def auto_mark_overdue():
    """
    Cronjob task to automatically mark borrowed items as overdue.
    """
    logger.info("Running auto mark overdue task")
    # TODO: Implement auto mark overdue logic
    return True

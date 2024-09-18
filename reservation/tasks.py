from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, default_retry_delay=5)
def send_email_to_customer(self, customer_email, reservation_details):
    try:
        subject = 'Your Reservation Details'
        message = f"Dear customer, here are your reservation details: {reservation_details}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [customer_email]
        
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        return self.retry(exc=e, max_retries=10)

@shared_task(bind=True, default_retry_delay=5)
def send_email_to_admin(self, reservation_details, admin_email):
    try:
        subject = 'New Reservation Alert'
        message = f"A new reservation has been made. Details: {reservation_details}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [admin_email]

        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        return self.retry(exc=e, max_retries=10)

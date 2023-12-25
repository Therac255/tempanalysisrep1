from django.conf import settings
from django.core.mail import send_mail

from app.celery import app


@app.task(
    retry_kwargs={
        "max_retries": 10,
        "countdown": 5,
    },
    acks_late=True,
)
def send_email_message(subject: str, email: str, message: str) -> None:
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],
              fail_silently=False)

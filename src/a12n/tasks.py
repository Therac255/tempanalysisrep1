
from a12n.services.otp import OTPMailSendService, OTPPhoneSendService
from app.celery import app


@app.task(
    retry_kwargs={
        "max_retries": 10,
        "countdown": 5,
    },
    acks_late=True,
)
def send_message_to_email(subject: str, email: str, message: str, allow_log: bool = True) -> None:

    OTPMailSendService(
        subject=subject,
        contact_value=email,
        message=message,
        allow_log=allow_log,
    )()


@app.task(
    retry_kwargs={
        "max_retries": 10,
        "countdown": 5,
    },
    acks_late=True,
)
def send_message_to_phone(phone_number: str, message: str) -> None:
    OTPPhoneSendService(
        contact_value=phone_number,
        message=message,
    )()

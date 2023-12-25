import asyncio
from dataclasses import dataclass
from typing import Any, Optional

from django.conf import settings
from django.core.mail import send_mail
from django_fsm import TransitionNotAllowed
from rest_framework.exceptions import ValidationError

from a12n.models import OTP
from a12n.services.a2p_sms import ServiceSMS
from a12n.services.sms import config
from app.services import BaseService
from users.email_templates import otp_auth_code
from users.models import User


@dataclass
class BaseOTPService(BaseService):
    contact_value: str
    message: str = ''
    notifications_template: str = otp_auth_code
    subject: str = ''
    allow_log: bool = True

    def act(self) -> Any:
        raise NotImplementedError()

    def create_otp(self, contact_type) -> None:
        user = self.get_user(contact_type)
        if not user:
            return
        contact_type = self.prepare_contact_type(contact_type)
        OTP.objects.update_or_create(   # TODO нихуя не понял для чего ты юзаешь этот метод!!! у тебя ниже логика пошла по пизде!!!
            user=user,
            **{contact_type: self.contact_value,
               'otp_code': self.message}
        )

    def send_otp(self, otp_type) -> None:
        context = {'code': self.message}
        if otp_type == 'email':
            send_mail(
                subject=self.subject,
                message=self.notifications_template.format(**context),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.contact_value],
                fail_silently=False
            )
        elif otp_type == 'phone':
            if isinstance(self.contact_value, str):
                target = self.contact_value
            else:
                target = self.contact_value.as_international
            sms_service = ServiceSMS(config.A2P_LOGIN, config.A2P_PASS)
            asyncio.run(
                sms_service.post_mes(self.notifications_template.format(**context),
                                     target, config.A2P_SENDER_NAME))

    def get_user(self, field) -> Optional[User]:
        try:
            return User.objects.get(**{field: self.contact_value})
        except User.DoesNotExist:
            return None

    def verify_otp(self, contact_type) -> None:
        contact_type = self.prepare_contact_type(contact_type)
        queryset = OTP.objects.filter(
            **{contact_type: self.contact_value}
        ).order_by('-sent').first()
        if queryset is None:
            raise ValidationError(
                "OTP with this contact does not exist"
            )

        queryset.check_otp(otp_code=self.message)
        queryset.is_used = True
        try:
            queryset.user.personal_info.verified()
        except TransitionNotAllowed:
            pass
        queryset.save()

    @staticmethod
    def prepare_contact_type(contact_type: str) -> str:
        """
        Prepares contact_type value for further usage personal_info__phone_number -> phone_number
        """
        if contact_type == 'personal_info__phone_number':
            return contact_type.split('__')[-1]
        return contact_type

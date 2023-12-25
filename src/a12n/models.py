import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import NotAcceptable

from app.models import TimestampedModel
from users.models import User


class OTP(TimestampedModel):
    """
    The `OTP` class represents a model for storing information about OTP.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Пользователь")
    )
    phone_number = PhoneNumberField(verbose_name=_("Номер телефона"), null=True, blank=True)
    email = models.EmailField(verbose_name=_("Email"), blank=True, null=True)
    otp_code = models.CharField(max_length=10, verbose_name=_("Код подтверждения почты"))
    is_used = models.BooleanField(default=False, verbose_name=_("Использовано"))
    sent = models.DateTimeField(verbose_name=_("Время отправки кода"), auto_now_add=True)

    class Meta:
        verbose_name = _("OTP")
        verbose_name_plural = _("OTP")

    def __str__(self):
        email = self.email if self.email and self.email else ''
        phone_number = self.phone_number if self.phone_number else ''
        return f"{email} - {phone_number} - {self.otp_code} - {self.sent} - {self.is_used}"

    def is_security_code_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            minutes=settings.OTP_EXPIRATION_TIME
        )

        return expiration_date <= timezone.now()

    def check_otp(self, otp_code):
        if self.is_security_code_expired():
            raise NotAcceptable(_("Код подтверждения истек"))
        if self.otp_code != otp_code:
            raise NotAcceptable(_("Неверный код подтверждения"))
        return True

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel
from users.models import User


class Buyer(TimestampedModel):
    """
    Represents a buyer.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tax_id = models.CharField(_("ИНН"), blank=True, null=True)

    class Meta:
        db_table = "buyer"
        verbose_name = _("Покупатель")
        verbose_name_plural = _("Покупатели")

    def __str__(self):
        if hasattr(self.user, 'personal_info'):
            return f"{self.user.personal_info.first_name} {self.user.personal_info.last_name}"
        return self.user.email

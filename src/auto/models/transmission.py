from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint

from auto.models.base import NamedBaseModel


class Transmission(NamedBaseModel):
    """
    A class representing a Transmission type in a Django application.

    Attributes:
        - name: The name of the Transmission type.
    """

    class Meta(NamedBaseModel.Meta):
        db_table = "transmission"
        verbose_name = _("Тип КПП")
        verbose_name_plural = _("Тип КПП")
        constraints = [
            UniqueConstraint(fields=["name"], name="unique_transmission_name")
        ]

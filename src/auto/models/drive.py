from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel


class Drive(NamedBaseModel):
    """
    The Drive class represents a physical drive in a system.

    Attributes:
        name (CharField): The name of the drive.
    """

    class Meta(NamedBaseModel.Meta):
        db_table = "drive"
        verbose_name = _("Привод")
        verbose_name_plural = _("Привод")
        constraints = [
            UniqueConstraint(fields=["name"], name="unique_drive_name")
        ]

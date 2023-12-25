from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint

from auto.models.base import NamedBaseModel


class CarColor(NamedBaseModel):
    """
    A class representing a car color.

    Attributes:
        name (CharField): The name of the car color.
    """

    class Meta(NamedBaseModel.Meta):
        db_table = "car_color"
        verbose_name = _("Цвет")
        verbose_name_plural = _("Цвета")
        constraints = [
            UniqueConstraint(fields=["name"], name="unique_color_name")
        ]

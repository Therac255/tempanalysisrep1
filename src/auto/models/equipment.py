from django.db import models
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel


class Equipment(NamedBaseModel):
    """
    A representation of a piece of equipment.
    """

    car = models.ForeignKey(
        "auto.Car",
        on_delete=models.SET_NULL,
        verbose_name=_("Модель авто"),
        related_name="car_equipment",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "equipment"
        verbose_name = _("Комплектация")
        verbose_name_plural = _("Комплектации")
        constraints = [
            models.UniqueConstraint(fields=["name", "car"], name="unique_car_equipment_name")
        ]
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)

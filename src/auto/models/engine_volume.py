from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel


class EngineVolume(TimestampedModel):
    """
    Module: EngineVolume

    This module contains the definition of the `EngineVolume` class,
    which represents the engine volume in a car.
    """

    volume = models.FloatField(verbose_name=_("Объем"))

    def __str__(self):
        return f"{self.volume}"

    class Meta:
        db_table = "engine_volume"
        verbose_name = _("Объем двигателя")
        verbose_name_plural = _("Объемы двигателей")
        constraints = [
            models.UniqueConstraint(fields=["volume"], name="unique_engine_volume")
        ]

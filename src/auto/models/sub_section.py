from django.db import models
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel
from auto.models.equipment import Equipment


class Subsection(NamedBaseModel):
    """
    Subsection model represents a subsection of equipment in the database.

    Attributes:
        name (str): The name of the subsection.
        equipment (ForeignKey): The equipment this subsection belongs to.
    """

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name=_("Комплектация"),
        related_name="subsections",
    )

    class Meta:
        db_table = "subsection"
        verbose_name = _("Подраздел")
        verbose_name_plural = _("Подразделы")
        constraints = [
            models.UniqueConstraint(fields=["name", "equipment"], name="unique_equipment_subsection_name")
        ]

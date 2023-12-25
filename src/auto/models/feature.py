from django.db import models
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel
from auto.models.sub_section import Subsection


class Feature(NamedBaseModel):
    """
    A class that represents a feature.

    Attributes:
        name (str): The name of the feature.
        subsection (Subsection): The subsection that the feature belongs to.
    """

    subsection = models.ForeignKey(
        Subsection,
        on_delete=models.CASCADE,
        verbose_name=_("Подраздел"),
        related_name="features",
    )

    class Meta:
        db_table = "feature"
        verbose_name = _("Функция")
        verbose_name_plural = _("Функции")
        constraints = [
            models.UniqueConstraint(fields=["name", "subsection"], name="unique_subsection_feature_name")
        ]

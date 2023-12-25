from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel


class EngineType(NamedBaseModel):
    """
    EngineType Class Documentation
    """

    class Meta(NamedBaseModel.Meta):
        db_table = "engine_type"
        verbose_name = _("Тип двигателя")
        verbose_name_plural = _("Типы двигателей")
        constraints = [
            UniqueConstraint(fields=["name"], name="unique_engine_type_name")
        ]

from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel


class BodyType(NamedBaseModel):
    """
    Attributes:
        name (CharField): The name of the body type.
    """

    class Meta(NamedBaseModel.Meta):
        db_table = "body_type"
        verbose_name = _("Тип кузова")
        verbose_name_plural = _("Типы кузова")

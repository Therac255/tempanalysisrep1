from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel


class Country(NamedBaseModel):
    """
    Model representing a country of origin for products.

    Attributes:
        name (CharField): The name of the country.
    """

    class Meta(NamedBaseModel.Meta):
        db_table = "country"
        verbose_name = _("Страна сборки")
        verbose_name_plural = _("Страны сборки")
        constraints = [
            UniqueConstraint(fields=["name"], name="unique_country_name")
        ]

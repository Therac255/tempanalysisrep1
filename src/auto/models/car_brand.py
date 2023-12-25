from django.db import models
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel


class CarBrand(NamedBaseModel):
    """
    A class representing a car brand in a Django application.

    Attributes:
        icon (FileField): An image field representing the brand's icon.
    """

    icon = models.FileField(verbose_name=_("Иконка"), upload_to="icons/", validators=[])
    is_popular = models.BooleanField(verbose_name=_("Популярный"), default=False)

    def sorted_brand_models(self):
        return self.cars_brand_model.all().order_by('name')

    class Meta(NamedBaseModel.Meta):
        db_table = "car_brand"
        verbose_name = _("Марка")
        verbose_name_plural = _("Марки")
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_brand_name")
        ]
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)

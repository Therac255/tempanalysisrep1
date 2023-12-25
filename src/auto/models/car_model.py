from django.db import models
from django.utils.translation import gettext_lazy as _

from auto.models.base import NamedBaseModel
from auto.models.car_brand import CarBrand


class CarModel(NamedBaseModel):
    """
    Module: car_model.py

    This module contains the CarModel class.
    """

    brand = models.ForeignKey(
        CarBrand,
        verbose_name=_("Марка"),
        related_name="cars_brand_model",
        on_delete=models.CASCADE,
    )
    is_popular = models.BooleanField(verbose_name=_("Популярный"), default=False)

    class Meta(NamedBaseModel.Meta):
        db_table = "car_model"
        verbose_name = _("Модель")
        verbose_name_plural = _("Модели")
        constraints = [
            models.UniqueConstraint(fields=["name", "brand"], name="unique_brand_model_name")
        ]
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)

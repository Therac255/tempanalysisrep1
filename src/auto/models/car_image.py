from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel
from auto.models.car import Car
from common.validators import validate_file_extension


class CarImage(TimestampedModel):
    """

    This class represents a CarImage model in the database.

    Attributes:
        image (FileField): The image file representing the car photo.
        car (ForeignKey): The foreign key to the Car model,
        representing the car that the image belongs to.
    """

    image = models.FileField(verbose_name=_("Фото"), upload_to="cars/photos/", validators=[validate_file_extension])
    car = models.ForeignKey(Car, related_name="car_images", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.car.model.name

    class Meta:
        db_table = "car_image"
        verbose_name = _("Фото")
        verbose_name_plural = _("Фото")

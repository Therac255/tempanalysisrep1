from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel
from auto.models.vin import Vin
from common.validators import validate_file_extension


class TechnicalImage(TimestampedModel):
    image = models.FileField(
        _("Технические фотографии"),
        upload_to="car_ad_images/",
        validators=[validate_file_extension]
    )
    vin = models.ForeignKey(Vin, on_delete=models.CASCADE, related_name="car_ad_images")

    class Meta:
        db_table = "technical_image"
        verbose_name = _("Техническое фото объявления")
        verbose_name_plural = _("Технические фото объявления")

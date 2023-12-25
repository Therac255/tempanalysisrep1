from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel
from auto.models.offer import Offer


class OfferImage(TimestampedModel):
    """
    The OfferImage class represents an image that belongs to an Offer object.

    Attributes:
        - image (FileField): The file field for the image.
        - offer (ForeignKey): The foreign key to the Offer model for the associated offer.
    """

    image = models.FileField(_("Фотографии от продавца"), upload_to="offer_images/")
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="offer_images"
    )

    class Meta:
        db_table = "offer_image"
        verbose_name = _("Фотография предложения")
        verbose_name_plural = _("Фотографии предложений")

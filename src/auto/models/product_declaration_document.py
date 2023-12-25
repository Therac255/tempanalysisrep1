from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel
from auto.models.vin import Vin


class ProductDeclarationDocument(TimestampedModel):
    file = models.FileField(_("Декларация на товары"), upload_to="product_declaration_documents/")
    vin = models.ForeignKey(Vin, on_delete=models.CASCADE, related_name="product_declaration_documents")

    class Meta:
        db_table = "product_declaration_document"
        verbose_name = _("Декларация на товары")
        verbose_name_plural = _("Декларация на товары")

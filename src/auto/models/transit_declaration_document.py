from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel
from auto.models.vin import Vin


class TransitDeclarationDocument(TimestampedModel):
    document = models.FileField(
        _("Документы транзитной декларации"), upload_to="transit_declaration_documents/"
    )
    vin = models.ForeignKey(
        Vin, on_delete=models.CASCADE, related_name="transit_declaration_documents"
    )

    class Meta:
        db_table = "transit_declaration_document"
        verbose_name = _("Документ транзитной декларации")
        verbose_name_plural = _("Документы транзитной декларации")

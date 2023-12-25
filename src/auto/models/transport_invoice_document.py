from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel
from auto.models.vin import Vin


class TransportInvoiceDocument(TimestampedModel):
    file = models.FileField(_("Товарно-транспортная накладная"), upload_to="transport_invoice_documents/")
    vin = models.ForeignKey(Vin, on_delete=models.CASCADE, related_name="transport_invoice_documents")

    class Meta:
        db_table = "transport_invoice_document"
        verbose_name = _("Товарно-транспортная накладная")
        verbose_name_plural = _("Товарно-транспортные накладные")

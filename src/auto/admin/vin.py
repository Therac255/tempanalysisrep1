from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from auto.forms import VinForm
from auto.models import (
    ProductDeclarationDocument,
    TechnicalImage,
    TransitDeclarationDocument,
    TransportInvoiceDocument,
    Vin,
)


class TransitDeclarationDocumentInline(admin.TabularInline):
    model = TransitDeclarationDocument
    extra = 1


class TechnicalImageInline(admin.TabularInline):
    model = TechnicalImage
    max_num = 20
    extra = 1


class ProductDeclarationDocumentInline(admin.TabularInline):
    model = ProductDeclarationDocument
    extra = 1


class TransportInvoiceDocumentInline(admin.TabularInline):
    model = TransportInvoiceDocument
    extra = 1


@admin.register(Vin)
class VinAdmin(admin.ModelAdmin):
    autocomplete_fields = ('car', 'offer')
    form = VinForm
    list_display = (
        "vin_code",
        "car",
        "equipment",
        "offer",
        "invoice",
        "packing_list",
        "CMR",
        "customs_inspection_report",
        "seller_proxy_to_broker",
        "handover_act",
        "contract",
        "status",
    )
    ordering = ("vin_code",)
    search_fields = ("vin_code", "status")
    list_filter = ("status", "car", "equipment", "offer")
    inlines = [
        TransitDeclarationDocumentInline,
        TechnicalImageInline,
        ProductDeclarationDocumentInline,
        TransportInvoiceDocumentInline,
    ]

    fieldsets = (
        (_("Основные поля"), {
            "fields": (
                "vin_code",
                "car",
                "equipment",
                "offer",
                "invoice",
                "packing_list",
                "CMR",
                "customs_inspection_report",
                "seller_proxy_to_broker",
                "handover_act",
                "contract",
                "status",
            ),
        }),
    )

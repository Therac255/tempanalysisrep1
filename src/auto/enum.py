from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class StatusChoices(TextChoices):
    NEEDS_MODERATION = 'needs_moderation', _('Требует модерации')
    MODERATED = 'moderated', _('Промодерирован на СВХ')
    RESERVED = 'reserved', _('Забронирован')
    PAID = 'paid', _('Оплачен')
    ISSUED = 'issued', _('Выдан')
    IN_TRANSIT = 'in_transit', _('В пути')
    READY = 'ready', _('Готов к выдаче')


class ModerationStates(TextChoices):
    ON_CHECK = "on_check", _("На проверке")
    APPROVED = "approved", _("Подтвержден")
    REJECTED = "rejected", _("Отклонено")


class PriceOrderingEnum(TextChoices):
    PRICE = "price"
    MINIMUM_PRICE = "minimum_price"
    DISCOUNTED_PRICE = "discounted_price"


class DocTypeEnum(TextChoices):
    INVOICE = "invoice"
    PACKING_LIST = "packing_list"
    CMR = "cmr"
    REPORT = "customs_inspection_report"
    SELLER_2_BROKER = "seller_proxy_to_broker"
    HANDOVER_ACT = "handover_act"
    CONTRACT = "contract"
    PRODUCT_DECLARATION_DOCUMENTS = "product_declaration_documents"
    TRANSIT_DECLARATION_DOCUMENTS = "transit_declaration_documents"
    TRANSPORT_INVOICE_DOCUMENTS = "transport_invoice_documents"

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from app.models import TimestampedModel
from auto.enum import StatusChoices
from auto.models.car import Car
from auto.models.equipment import Equipment

# from auto.models.offer import Offer


class Vin(TimestampedModel):
    vin_code = models.CharField(
        _("Код VIN"), max_length=17
    )
    car = models.ForeignKey(
        Car,
        verbose_name=_("Авто"),
        on_delete=models.PROTECT,
        related_name="vin_car"
    )
    equipment = models.ForeignKey(
        Equipment,
        verbose_name=_("Комплектация"),
        on_delete=models.PROTECT,
        related_name="vin_equipment"
    )
    offer = models.ForeignKey(
        "auto.Offer",
        verbose_name=_("Предложение"),
        on_delete=models.CASCADE,
        related_name="vin_offer"
    )
    invoice = models.FileField(
        _("Инвойс"), upload_to="invoice_files/", null=True, blank=True
    )
    packing_list = models.FileField(
        _("Упаковочный лист"), upload_to="packing_list_files/", null=True, blank=True
    )
    CMR = models.FileField(_("CMR"), upload_to="cmr_files/", null=True, blank=True)
    customs_inspection_report = models.FileField(
        _("Акт таможенного осмотра"),
        upload_to="customs_inspection_report_files/",
        null=True, blank=True
    )
    seller_proxy_to_broker = models.FileField(
        _("Доверенность продавца на брокера"),
        upload_to="seller_proxy_to_broker_files/",
        null=True, blank=True
    )
    handover_act = models.FileField(
        _("Акт приема - передачи"),
        upload_to="handover_act_files/",
        null=True, blank=True
    )
    contract = models.FileField(
        _("Договор"), upload_to="contract_files/",
        null=True, blank=True
    )
    status = FSMField(
        _("Статус"),
        max_length=30,
        choices=StatusChoices.choices,
        default=StatusChoices.NEEDS_MODERATION,
    )

    # Technical characteristics
    fuel_consumption = models.FloatField(
        verbose_name=_("Расход топлива"),
        default=0.0,
    )

    acceleration = models.FloatField(
        verbose_name=_("Разгон до 100 км/ч"),
        default=0.0,
    )

    length = models.IntegerField(
        verbose_name=_("Длина (мм)"),
        default=0,
    )

    height = models.IntegerField(
        verbose_name=_("Высота (мм)"),
        default=0,
    )

    clearance = models.IntegerField(
        verbose_name=_("Дорожный просвет (мм)"),
        default=0,
    )

    wheelbase = models.IntegerField(
        verbose_name=_("Колёсная база (мм)"),
        default=0,
    )

    front_track = models.IntegerField(
        verbose_name=_("Колея передняя (мм)"),
        default=0,
    )

    rear_track = models.IntegerField(
        verbose_name=_("Колея задняя (мм)"),
        default=0,
    )

    front_tire_size = models.CharField(
        verbose_name=_("Размерность передних шин"),
        max_length=100,
        default=0,
    )

    rear_tire_size = models.CharField(
        verbose_name=_("Размерность задних шин"),
        max_length=100,
        default=0,
    )

    engine_displacement = models.IntegerField(
        verbose_name=_("Рабочий объем двигателя (см куб)"),
        default=0,
    )

    num_of_cylinders = models.IntegerField(
        verbose_name=_("Количество цилиндров"),
        default=0,
    )

    front_brakes = models.BooleanField(
        verbose_name=_("Передние тормоза"),
        default=False
    )

    rear_brakes = models.BooleanField(
        verbose_name=_("Задние тормоза"),
        default=False
    )

    num_of_doors = models.IntegerField(
        verbose_name=_("Количество дверей"),
        default=0,
    )

    euroNCAP_rating = models.IntegerField(
        verbose_name=_("Рейтинг EuroNCAP"),
        default=0,
    )

    def save(self, *args, **kwargs):
        """
        Copy technical characteristics from offer to vin
        """
        fields = [
            'fuel_consumption',
            'acceleration',
            'length',
            'height',
            'clearance',
            'wheelbase',
            'front_track',
            'rear_track',
            'front_tire_size',
            'rear_tire_size',
            'engine_displacement',
            'num_of_cylinders',
            'front_brakes',
            'rear_brakes',
            'num_of_doors',
            'euroNCAP_rating'
        ]

        if self.pk is None:  # Only during creation
            for field in fields:
                setattr(self, field, getattr(self.offer, field))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vin_code}"

    class Meta:
        db_table = "vin"
        verbose_name = _("VIN")
        verbose_name_plural = _("VIN")

    @transition(field="status", source=StatusChoices.NEEDS_MODERATION, target=StatusChoices.MODERATED)
    def moderated(self):
        pass

    @transition(field="status", source=StatusChoices.MODERATED, target=StatusChoices.RESERVED)
    def reserved(self):
        pass

    @transition(field="status", source=StatusChoices.RESERVED, target=StatusChoices.PAID)
    def paid(self):
        pass

    @transition(field="status", source=StatusChoices.PAID, target=StatusChoices.IN_TRANSIT)
    def transferred(self):
        pass

    @transition(field="status", source=StatusChoices.IN_TRANSIT, target=StatusChoices.READY)
    def ready(self):
        pass

    @transition(field="status", source=StatusChoices.READY, target=StatusChoices.ISSUED)
    def issued(self):
        pass

    @transition(field="status",
                source=[StatusChoices.RESERVED,
                        StatusChoices.PAID,
                        StatusChoices.IN_TRANSIT,
                        StatusChoices.READY,
                        StatusChoices],
                target=StatusChoices.MODERATED)
    def cancelled(self):
        pass

    @transition(
        status,
        source=[
            StatusChoices.MODERATED,
            StatusChoices.NEEDS_MODERATION
        ],
        target=StatusChoices.NEEDS_MODERATION
    )
    def on_check(self):
        pass

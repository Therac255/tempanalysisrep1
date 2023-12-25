from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from app.models import TimestampedModel
from auto.enum import ModerationStates
from auto.models.car import Car
from auto.models.equipment import Equipment
from seller.models import Seller


class Offer(TimestampedModel):
    """
    Class: Offer

    A model representing an offer made by a seller for a car with specific equipment.

    Attributes:
    - seller (ForeignKey): The seller making the offer.
    - car (ForeignKey): The car being offered.
    - equipment (ForeignKey): The equipment associated with the offer.
    - description (RichTextField): The description provided by the seller for the offer.
    - price (PositiveIntegerField): The cost of the offer.
    """

    seller = models.ForeignKey(
        Seller, verbose_name=_("Продавец"), on_delete=models.CASCADE,
        related_name="offers"
    )
    car = models.ForeignKey(Car, verbose_name=_("Авто"), on_delete=models.CASCADE, related_name="car_offers")
    equipment = models.ForeignKey(
        Equipment,
        verbose_name=_("Комплектация"),
        on_delete=models.CASCADE,
        related_name='equipment_offers',
        blank=True,
        null=True,
    )
    description = RichTextField(verbose_name=_("Описание от продавца"))
    price = models.PositiveIntegerField(_("Стоимость"), default=0)
    discounted_price = models.PositiveIntegerField(_("Стоимость со скидкой"), default=0)

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
        help_text=_("(без галочки ободные, с галочкой дисковые)"),
        default=False
    )

    rear_brakes = models.BooleanField(
        verbose_name=_("Задние тормоза"),
        help_text=_("(без галочки ободные, с галочкой дисковые)"),
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
    state = FSMField(
        _("Состояние"),
        choices=ModerationStates.choices,
        default=ModerationStates.ON_CHECK
    )

    def save(self, *args, **kwargs):
        """
        Saves the Offer instance to the database.

        Copy the technical characteristics from the car to the offer.
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
                setattr(self, field, getattr(self.car, field))

        super().save(*args, **kwargs)

    class Meta:
        db_table = "offer"
        verbose_name = _("Предложение")
        verbose_name_plural = _("Предложения")
        unique_together = ("seller", "car", "equipment")

    def __str__(self):
        return f"{self.seller} {self.car} {self.equipment}"

    @transition(
        state,
        source=ModerationStates.ON_CHECK,
        target=ModerationStates.APPROVED
    )
    def approved(self, *args, **kwargs):
        pass

    @transition(
        state,
        source=ModerationStates.ON_CHECK,
        target=ModerationStates.REJECTED
    )
    def rejected(self, *args, **kwargs):
        print("rejected")  # noqa

    @transition(
        state,
        source=[
            ModerationStates.APPROVED,
            ModerationStates.REJECTED,
            ModerationStates.ON_CHECK
        ],
        target=ModerationStates.ON_CHECK)
    def on_check(self, *args, **kwargs):
        pass

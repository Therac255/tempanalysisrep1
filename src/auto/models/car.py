from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from app.models import TimestampedModel
from auto.enum import StatusChoices, ModerationStates
from auto.models.body_type import BodyType
from auto.models.car_brand import CarBrand
from auto.models.car_color import CarColor
from auto.models.car_model import CarModel
from auto.models.country import Country
from auto.models.drive import Drive
from auto.models.engine_type import EngineType
from auto.models.engine_volume import EngineVolume
from auto.models.transmission import Transmission


class Car(TimestampedModel):
    """
    The Car class represents a car object with various attributes such as brand,
    model, body type, color, engine type, engine volume, transmission type,
    drive type, assembly country, manufacturing year, horsepower, and steering side.
    """

    brand = models.ForeignKey(
        CarBrand,
        verbose_name=_("Марка"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_brand",
    )
    model = models.ForeignKey(
        CarModel,
        verbose_name=_("Модель"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_model",
    )
    body_type = models.ForeignKey(
        BodyType,
        verbose_name=_("Тип кузова"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_body_type",
    )
    color = models.ForeignKey(
        CarColor,
        verbose_name=_("Цвет"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_color",
    )
    engine_type = models.ForeignKey(
        EngineType,
        verbose_name=_("Тип двигателя"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_engine_type",
    )
    engine_volume = models.ForeignKey(
        EngineVolume,
        verbose_name=_("Объем двигателя"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_engine_volume",
    )
    transmission_type = models.ForeignKey(
        Transmission,
        verbose_name=_("Тип КПП"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_transmission_type",
    )
    drive_type = models.ForeignKey(
        Drive,
        verbose_name=_("Привод"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_drive_type",
    )
    assembly_country = models.ForeignKey(
        Country,
        verbose_name=_("Страна сборки"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="cars_assembly_country",
    )
    manufacturing_year = models.PositiveIntegerField(verbose_name=_("Год выпуска"))
    horsepower = models.PositiveIntegerField(
        verbose_name=_("Лошадиные силы"),
        validators=[MaxValueValidator(1000)],
        default=0
    )
    steering_side = models.BooleanField(
        verbose_name=_("Cторона руля (без галочки правый руль)"),
        default=True,
    )  # True for left side
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

    status = FSMField(
        choices=ModerationStates.choices,
        default=ModerationStates.ON_CHECK
    )

    def __str__(self):
        return (
            f"Бренд - {self.brand}, "
            f"Модель - {self.model}, "
            f"Тип кузова - {self.body_type}, "
            f"Цвет - {self.color}, "
            f"Тип двигателя - {self.engine_type}, "
            f"Объем двигателя - {self.engine_volume}, "
            f"Тип трансмиссии - {self.transmission_type}, "
            f"Тип привода - {self.drive_type}, "
            f"Страна сборки - {self.assembly_country}, "
            f"Год производства - {self.manufacturing_year}"
        )

    def get_moderated_offers(self):
        """
        Get all moderated offers for a car.
        With exists() we check if there are any offers with status MODERATED.
        """
        moderated_offers = self.car_offers.filter(vin_offer__status=StatusChoices.MODERATED)
        return moderated_offers

    def get_price(self):
        """
        Get the price of the car from all offers.
        """
        moderated_offers = self.get_moderated_offers()
        if not moderated_offers:
            return 0

        first_offer = moderated_offers.order_by('price').first()
        return first_offer.price if first_offer else 0

    def get_discounted_price(self):
        """
        Get discounted price for a car from all offers.
        """
        moderated_offers = self.get_moderated_offers()
        if not moderated_offers:
            return 0
        first_offer = moderated_offers.order_by(
            models.Case(
                models.When(
                    discounted_price__gt=0,
                    then=models.F("discounted_price")
                ),
                default=models.F("price")
            )).first()

        return first_offer.discounted_price if first_offer else 0

    def get_minimum_price(self):
        """
        Returns the minimum price of a car from price and discounted price.
        Get minimum price for a car from all offers have vin with status MODERATED.
        """

        # moderated_offers = self.get_moderated_offers()
        # if not moderated_offers:
        #     return 0
        # first_offer = moderated_offers.order_by('discounted_price').first()
        return self.get_price() if self.get_discounted_price() == 0 else self.get_discounted_price()

    class Meta:
        db_table = "car"
        ordering = ["-vin_car__created"]
        verbose_name = _("Авто")
        verbose_name_plural = _("Авто")
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'brand',
                    'model',
                    'body_type',
                    'color',
                    'engine_type',
                    'engine_volume',
                    'transmission_type',
                    'drive_type',
                    'assembly_country',
                    'manufacturing_year',
                    'steering_side',
                    "status"
                ],
                name='unique_car'
            ),
        ]

    @transition(
        field=status,
        source=ModerationStates.ON_CHECK,
        target=ModerationStates.APPROVED
    )
    def approved(self):
        pass
    
    @transition(
        field=status,
        source=ModerationStates.ON_CHECK,
        target=ModerationStates.REJECTED
    )
    def rejected(self):
        pass

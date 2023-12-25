# mypy: ignore-errors
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from auto.forms import OfferForm
from auto.models import Offer, OfferImage


class OfferImageInline(admin.TabularInline):
    model = OfferImage
    max_num = 5
    extra = 1


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    autocomplete_fields = ('car', 'equipment')
    form = OfferForm
    list_display = (
        "id",
        "seller",
        "car",
        "equipment",
        "description",
        "price",
        "discounted_price",
        "state"
    )
    search_fields = (
        "description",
        "seller__user__personal_info__first_name",
        "equipment__name",
        "state",
        "car__brand__name",
        "car__model__name",
        "car__body_type__name",
        "car__color__name",
        "car__engine_type__name",
        "car__engine_volume__volume",
        "car__transmission_type__name",
        "car__drive_type__name",
        "car__assembly_country__name",
        "car__manufacturing_year",
        "car__steering_side",
        "car__horsepower",
    )
    list_filter = (
        'seller__user__personal_info__first_name',
        'car__brand__name',
        'equipment__name',
        "state"
    )
    inlines = [OfferImageInline]

    fieldsets = (
        (_("Основные поля"), {
            "fields": (
                "seller",
                "car",
                "equipment",
                "description",
                "price",
                "discounted_price",
                "state"
            ),
        }),
        (_("Технические характеристики"), {
            "fields": (
                "fuel_consumption",
                "acceleration",
                "length",
                "height",
                "clearance",
                "wheelbase",
                "front_track",
                "rear_track",
                "front_tire_size",
                "rear_tire_size",
                "engine_displacement",
                "num_of_cylinders",
                "front_brakes",
                "rear_brakes",
                "num_of_doors",
                "euroNCAP_rating",
            ),
        })
    )

    def seller_first_name(self, obj):
        return obj.seller.user.first_name

    seller_first_name.short_description = "Имя"

    def car_brand_name(self, obj):
        return obj.car.brand.name

    car_brand_name.short_description = "Имя брэнда"

    def equipment_name(self, obj):
        return obj.car.brand.name

    equipment_name.short_description = "Комплектация"

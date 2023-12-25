# mypy: ignore-errors
from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from auto.models import Equipment, Feature, Subsection


class FeatureInline(NestedStackedInline):
    model = Feature
    extra = 1


class SubsectionInline(NestedStackedInline):
    model = Subsection
    extra = 1
    inlines = [FeatureInline]


@admin.register(Equipment)
class EquipmentAdmin(NestedModelAdmin):
    autocomplete_fields = ('car',)
    list_display = (
        "name",
        "car_brand_name",
        "car_brand_model_name",
        "car_body_type",
        "car_color",
        "car_engine_type",
        "car_engine_volume",
        "car_transmission_type",
        "car_drive_type",
        "car_assembly_country",
        "car_manufacturing_year",
        "car_steering_side",
        "car_horsepower",

    )
    search_fields = (
        "name",
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
        "car__brand__name",
        "car__model__name",
        "car__body_type",
        "car__color",
        "car__engine_type",
        "car__engine_volume",
        "car__transmission_type",
        "car__drive_type",
        "car__assembly_country",
        "car__manufacturing_year",
        "car__steering_side",
        "car__horsepower",
    )
    inlines = [SubsectionInline]

    def car_brand_name(self, obj):
        return obj.car.brand.name if obj.car and obj.car.brand.name else ''
    car_brand_name.admin_order_field = 'car__brand_name'
    car_brand_name.short_description = 'Марка'

    def car_brand_model_name(self, obj):
        return obj.car.model.name if obj.car and obj.car.model.name else ''
    car_brand_model_name.admin_order_field = 'car__brand_model'
    car_brand_model_name.short_description = 'Модель'

    def car_body_type(self, obj):
        return obj.car.body_type if obj.car and obj.car.body_type else ''
    car_body_type.admin_order_field = 'car__body_type'
    car_body_type.short_description = 'Тип кузова'

    def car_color(self, obj):
        return obj.car.color if obj.car and obj.car.color else ''
    car_color.admin_order_field = 'car__color'
    car_color.short_description = 'Цвет'

    def car_engine_type(self, obj):
        return obj.car.engine_type if obj.car and obj.car.engine_type else ''
    car_engine_type.admin_order_field = 'car__engine_type'
    car_engine_type.short_description = 'Тип двигателя'

    def car_engine_volume(self, obj):
        return obj.car.engine_volume if obj.car and obj.car.engine_volume else ''
    car_engine_volume.admin_order_field = 'car__engine_volume'
    car_engine_volume.short_description = 'Объем двигателя'

    def car_transmission_type(self, obj):
        return obj.car.transmission_type if obj.car and obj.car.transmission_type else ''
    car_transmission_type.admin_order_field = 'car__transmission_type'
    car_transmission_type.short_description = 'Тип трансмиссии'

    def car_drive_type(self, obj):
        return obj.car.drive_type if obj.car and obj.car.drive_type else ''
    car_drive_type.admin_order_field = 'car__drive_type'
    car_drive_type.short_description = 'Тип привода'

    def car_assembly_country(self, obj):
        return obj.car.assembly_country if obj.car and obj.car.assembly_country else ''
    car_assembly_country.admin_order_field = 'car__assembly_country'
    car_assembly_country.short_description = 'Страна сборки'

    def car_manufacturing_year(self, obj):
        return obj.car.manufacturing_year if obj.car and obj.car.manufacturing_year else ''
    car_manufacturing_year.admin_order_field = 'car__manufacturing_year'
    car_manufacturing_year.short_description = 'Год выпуска'

    def car_steering_side(self, obj):
        return obj.car.steering_side if obj.car and obj.car.steering_side else ''
    car_steering_side.admin_order_field = 'car__steering_side'
    car_steering_side.short_description = 'Руль'

    def car_horsepower(self, obj):
        return obj.car.horsepower if obj.car and obj.car.horsepower else ''
    car_horsepower.admin_order_field = 'car__horsepower'
    car_horsepower.short_description = 'Мощность'

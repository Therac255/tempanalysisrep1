from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportMixin

from auto.models import (
    BodyType,
    Car,
    CarBrand,
    CarColor,
    CarImage,
    CarModel,
    Drive,
    EngineType,
    EngineVolume,
    Transmission,
)
from auto.resourse import CarResource
from orders.forms import CarForm
from orders.models import AdditionalServices


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "icon",
    )
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
    )
    list_filter = ("brand",)
    search_fields = (
        "name",
        "brand__name",
    )
    ordering = (
        "brand",
        "name",
    )


@admin.register(BodyType)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(EngineVolume)
class EngineVolumeAdmin(admin.ModelAdmin):
    list_display = ("volume",)
    ordering = ("volume",)


@admin.register(Transmission)
class TransmissionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Drive)
class DriveAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    max_num = 5  # Maximum number of images that can be uploaded for a car.


class AdditionalServicesInline(admin.TabularInline):
    model = AdditionalServices
    extra = 1
    exclude = (
        "order",
    )


@admin.register(Car)
class CarAdmin(ImportMixin, admin.ModelAdmin):
    change_form_template = "change_list.html"
    resource_class = CarResource
    form = CarForm
    list_display = (
        "brand",
        "model",
        "body_type",
        "color",
        "engine_type",
        "engine_volume",
        "transmission_type",
        "drive_type",
        "assembly_country",
        "manufacturing_year",
        "steering_side",
        "horsepower"
    )
    list_filter = (
        "brand",
        "model",
        "additional_services__service",
        "body_type",
        "color",
        "engine_type",
        "engine_volume",
        "transmission_type",
        "drive_type",
        "assembly_country",
        "manufacturing_year",
        "steering_side",
    )
    search_fields = (
        'car_equipment__name',
        "brand__name",
        "model__name",
        "body_type__name",
        "color__name",
        "engine_type__name",
        'engine_volume__volume',
        "transmission_type__name",
        "drive_type__name",
        "assembly_country__name",
        "manufacturing_year"
    )

    inlines = [
        CarImageInline, AdditionalServicesInline
    ]

    fieldsets = (
        (_("Основные характеристики"), {
            "fields": (
                "brand",
                "model",
                "body_type",
                "color",
                "engine_type",
                "engine_volume",
                "transmission_type",
                "drive_type",
                "assembly_country",
                "manufacturing_year",
                "steering_side",
                "horsepower",
                "status"
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
        }),
    )

    def get_ordering(self, request):
        return ['id']

    def response_change(self, request, obj):
        if "_copy_car_data" in request.POST:
            new_car = Car.objects.create(
                brand=obj.brand,
                model=obj.model,
                body_type=obj.body_type,
                color=obj.color,
                engine_type=obj.engine_type,
                engine_volume=obj.engine_volume,
                transmission_type=obj.transmission_type,
                drive_type=obj.drive_type,
                assembly_country=obj.assembly_country,
                manufacturing_year=obj.manufacturing_year,
                horsepower=obj.horsepower,
                steering_side=obj.steering_side,
                fuel_consumption=obj.fuel_consumption,
                acceleration=obj.acceleration,
                length=obj.length,
                height=obj.height,
                clearance=obj.clearance,
                wheelbase=obj.wheelbase,
                front_track=obj.front_track,
                rear_track=obj.rear_track,
                front_tire_size=obj.front_tire_size,
                rear_tire_size=obj.rear_tire_size,
                engine_displacement=obj.engine_displacement,
                num_of_cylinders=obj.num_of_cylinders,
                front_brakes=obj.front_brakes,
                rear_brakes=obj.rear_brakes,
                num_of_doors=obj.num_of_doors,
                euroNCAP_rating=obj.euroNCAP_rating,
            )

            return HttpResponseRedirect(f"/admin/auto/car/{new_car.id}/change/")
        return super().response_change(request, obj)

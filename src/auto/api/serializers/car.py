from rest_framework import serializers

from auto.api.serializers.car_image import CarImageSerializer
from auto.models import Car
from orders.api.serializers.additional_service import AdditionalServicesSerializer


class CarSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    model = serializers.StringRelatedField()
    body_type = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    engine_type = serializers.StringRelatedField()
    engine_volume = serializers.StringRelatedField()
    transmission_type = serializers.StringRelatedField()
    drive_type = serializers.StringRelatedField()
    assembly_country = serializers.StringRelatedField()
    price = serializers.CharField(source='get_price')
    discounted_price = serializers.CharField(source='get_discounted_price')
    minimum_price = serializers.CharField(source='get_minimum_price')
    additional_services = AdditionalServicesSerializer(many=True)
    car_images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id',
            'brand',
            'model',
            'body_type',
            'color',
            'engine_type',
            'car_images',
            'engine_volume',
            'transmission_type',
            'drive_type',
            'assembly_country',
            'manufacturing_year',
            'horsepower',
            'price',
            'discounted_price',
            'minimum_price',
            'additional_services',
            'steering_side',
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
            'euroNCAP_rating',
        ]


class CreateCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "id",
            "brand",
            "model",
            "manufacturing_year",
            "body_type",
            "color",
            "engine_type",
            "engine_volume",
            "transmission_type",
            "drive_type",
            "assembly_country",
            "steering_side",
            "horsepower"
        ]

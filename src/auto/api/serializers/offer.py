from rest_framework import serializers

from auto.api.serializers.car import CarSerializer
from auto.api.serializers.car_image import AbstractCreateImageSerializer, AbstractDeleteImageSerializer
from auto.api.serializers.equipment import EquipmentSerializer
from auto.api.serializers.offer_image import OfferImageSerializer
from auto.enum import ModerationStates, StatusChoices
from auto.models import Offer
from auto.models.offer_image import OfferImage
from seller.api.serializers import SellerSerializer


class OfferSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    equipment = EquipmentSerializer()
    seller = SellerSerializer()

    offer_images = OfferImageSerializer(many=True, read_only=True)
    available_vins = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'seller',
            'car',
            'equipment',
            'description',
            'price',
            'offer_images',
            'discounted_price',
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
            'available_vins'
        ]

    def get_available_vins(self, obj):
        return obj.car.vin_car.filter(
            offer=obj,
            car=obj.car,
            status__in=[StatusChoices.NEEDS_MODERATION, StatusChoices.MODERATED]
        ).count()


class CreateOfferSerializer(serializers.ModelSerializer):
    equipment_id = serializers.UUIDField(required=False)

    class Meta:
        model = Offer
        fields = [
            "id",
            "car",
            "equipment_id",
            "description",
            "price",
            "discounted_price",
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
            "euroNCAP_rating"
        ]

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["seller"] = user.seller
        return super().create(validated_data)


class UpdateOfferSerializer(serializers.ModelSerializer):
    car = serializers.UUIDField(required=False)
    equipment = serializers.UUIDField(required=False)
    description = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    discounted_price = serializers.CharField(required=False)
    fuel_consumption = serializers.CharField(required=False)
    acceleration = serializers.CharField(required=False)
    length = serializers.CharField(required=False)
    height = serializers.CharField(required=False)
    clearance = serializers.CharField(required=False)
    wheelbase = serializers.CharField(required=False)
    front_track = serializers.CharField(required=False)
    rear_track = serializers.CharField(required=False)
    front_tire_size = serializers.CharField(required=False)
    rear_tire_size = serializers.CharField(required=False)
    engine_displacement = serializers.CharField(required=False)
    num_of_cylinders = serializers.CharField(required=False)
    front_brakes = serializers.BooleanField(required=False)
    rear_brakes = serializers.BooleanField(required=False)
    num_of_doors = serializers.CharField(required=False)
    euroNCAP_rating = serializers.CharField(required=False)
    # offer_images = serializers.ListField(child=serializers.FileField(), required=False, write_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "car",
            "equipment",
            "description",
            "price",
            "discounted_price",
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
            # "offer_images"
        ]

    def update(self, instance: Offer, validated_data):
        car_id = validated_data.pop("car", None)
        equipment_id = validated_data.pop("equipment", None)
        if car_id:
            validated_data["car_id"] = car_id
        if equipment_id:
            validated_data["equipment_id"] = equipment_id

        # images = validated_data.pop("offer_images", None)
        # if images:
        #     images_ = [{"image": value, "offer": instance.id} for value in images]
        #     ser = OfferImageSerializer(
        #         data=images_,
        #         many=True
        #     )
        #     ser.is_valid(raise_exception=True)
        #     ser.save()
        validated_data["state"] = ModerationStates.ON_CHECK

        return super().update(instance, validated_data)


class OfferShortInfo(serializers.ModelSerializer):
    car_title = serializers.SerializerMethodField()
    price = serializers.FloatField(source="car.get_minimum_price")
    vin_count = serializers.IntegerField(source="car.vin_car.count")
    equipment = serializers.CharField(source="equipment.name")

    class Meta:
        model = Offer
        fields = [
            "id",
            "car_title",
            "price",
            "vin_count",
            "equipment"
        ]

    def get_car_title(self, obj):
        return f"{obj.car.brand} {obj.car.model}"


class VinImagesMixin:
    image_cls = OfferImage
    relation_field = "offer"


class CreateOfferImagesSerializer(VinImagesMixin, AbstractCreateImageSerializer):
    pass


class DeleteOfferImagesSerializer(VinImagesMixin, AbstractDeleteImageSerializer):
    pass

from collections import OrderedDict

import distutils
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from auto.models import BodyType, CarBrand, CarColor, CarModel, Country, Drive, EngineType, EngineVolume, Transmission


class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drive
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class TransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transmission
        fields = ['id', 'name']


class EngineVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineVolume
        fields = ['id', 'volume']


class EngineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineType
        fields = ['id', 'name']


class CarColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarColor
        fields = ['id', 'name']


class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = ['id', 'name']


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ['id', 'name', 'icon', 'is_popular']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'brand', 'is_popular']


class BrandCarModelSerializer(CarModelSerializer):
    brand = CarBrandSerializer()

    class Meta(CarModelSerializer.Meta):
        fields = CarModelSerializer.Meta.fields + ["brand"]


class BrandModelSerializer(CarModelSerializer):
    cars_brand_model = serializers.SerializerMethodField()

    class Meta:
        model = CarBrand
        fields = ["cars_brand_model"]

    def get_cars_brand_model(self, obj):
        queryset = obj.sorted_brand_models()
        return CarModelSerializer(instance=queryset, many=True).data

    def to_representation(self, instance):
        request = self.context["request"]

        is_popular = request.query_params.get("is_popular")
        if is_popular:
            is_popular = distutils.util.strtobool(is_popular)

        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                value = field.to_representation(attribute)

                indices = []
                for idx, model in enumerate(value):
                    if isinstance(is_popular, bool) and model.get("is_popular") != is_popular:
                        indices.append(idx)

                for idx in indices[::-1]:
                    value.pop(idx)

                ret[field.field_name] = value

        return ret


####

class CreateCarBrandModel(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = [
            "name",
            "icon"
        ]


class CreateCarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = [
            "name",
            "brand"
        ]

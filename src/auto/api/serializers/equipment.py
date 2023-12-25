from rest_framework import serializers

from auto.models import Equipment, Feature, Subsection


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name"]


class CreateFeatureSerializer(FeatureSerializer):
    class Meta(FeatureSerializer.Meta):
        fields = FeatureSerializer.Meta.fields + ["subsection"]


class SubsectionSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = Subsection
        fields = ["id", "name", "features"]


class CreateSubsectionSerializer(SubsectionSerializer):
    class Meta(SubsectionSerializer.Meta):
        fields = SubsectionSerializer.Meta.fields + ["equipment"]

    def create(self, validated_data):
        new_features = validated_data.pop("features")
        subsection = super().create(validated_data)
        updated_features = [
            {
                "subsection": subsection.id,
                **feature
            }
            for feature in new_features
        ]
        ser = CreateFeatureSerializer(
            data=updated_features,
            many=True
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        return subsection


class EquipmentSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="car.model.brand.name", read_only=True)
    model = serializers.CharField(source="car.model.name", read_only=True)
    subsections = SubsectionSerializer(many=True)

    class Meta:
        model = Equipment
        fields = ["id", "name", "brand", "model", "subsections"]


class CreateEquipmentSerializer(serializers.ModelSerializer):
    subsections = SubsectionSerializer(many=True)

    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "car",
            "subsections"
        ]

    def save(self, **kwargs):
        new_subsections = self.validated_data.pop("subsections", [])
        equipment = super().save()
        updated_subsections = [
            {
                "equipment": equipment.id,
                **subsection
            }
            for subsection in new_subsections
        ]
        ser = CreateSubsectionSerializer(
            data=updated_subsections,
            many=True
        )
        ser.is_valid(raise_exception=True)
        ser.save()

        return equipment

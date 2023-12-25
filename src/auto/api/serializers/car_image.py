from rest_framework import serializers
from django.db.models import Model
from django_fsm import TransitionNotAllowed

from auto.models import CarImage


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']


class MetaImageSerializer(serializers.Serializer):
    image_cls: Model
    relation_field = None
    class Meta:
        fields = ["images"]

    def save(self, **kwargs):
        try:
            self.instance.on_check()
        except TransitionNotAllowed:
            raise serializers.ValidationError(detail={"message": "Invalid state or status"})
        self.instance.save()


class AbstractCreateImageSerializer(MetaImageSerializer):
    images = serializers.ListField(child=serializers.FileField())

    def save(self, **kwargs):
        super().save()
        images = self.validated_data.get("images")
        updated_images = [
            self.image_cls(
                **{"image": image, self.relation_field: self.instance}
            )
            for image in images
        ]
        self.image_cls.objects.bulk_create(updated_images)


class AbstractDeleteImageSerializer(MetaImageSerializer):
    images = serializers.ListField(child=serializers.UUIDField())

    def save(self, **kwargs):
        super().save()
        ids = self.validated_data.get("images")
        self.image_cls.objects.filter(
            **{f"{self.relation_field}": self.instance, "id__in": ids}
        ).delete()

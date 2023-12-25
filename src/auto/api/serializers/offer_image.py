from rest_framework import serializers

from auto.models import OfferImage


class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferImage
        fields = ["id", "offer", 'image']

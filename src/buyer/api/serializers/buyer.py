from rest_framework import serializers

from buyer.models import Buyer
from users.api.serializers import UserSerializer, UserUpdatablePersonalInfoSerializer


class BuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Buyer
        fields = ['user', 'tax_id']


class BuyerPersonalInfoUpdateSerializer(serializers.ModelSerializer):
    personal_info = UserUpdatablePersonalInfoSerializer()
    tax_id = serializers.CharField(required=False)

    class Meta:
        model = Buyer
        fields = [
            "personal_info",
            "tax_id"
        ]

    def update(self, instance, validated_data):
        input_personal_info = validated_data.pop("personal_info", None)
        personal_info = instance.user.personal_info
        user_serializer = UserUpdatablePersonalInfoSerializer(
            instance=personal_info,
            data=input_personal_info
        )
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return super().update(instance=instance, validated_data=validated_data)


class BuyerDocumentUploadSerializer(serializers.ModelSerializer):
    document_scan = serializers.FileField()

    class Meta:
        model = Buyer
        fields = [
            "document_scan"
        ]

    def create(self):
        raise NotImplementedError

    def update(self, instance, validated_data):
        personal_info = instance.user.personal_info
        personal_info.document_scan = validated_data.get("document_scan")
        personal_info.save()
        return instance

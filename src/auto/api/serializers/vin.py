from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from auto.api.serializers.car import CarSerializer
from auto.api.serializers.car_image import AbstractCreateImageSerializer, AbstractDeleteImageSerializer
from auto.api.serializers.equipment import EquipmentSerializer
from auto.api.serializers.offer import OfferSerializer
from auto.enum import DocTypeEnum, StatusChoices
from auto.models import Offer, TechnicalImage, Vin
from auto.models.product_declaration_document import ProductDeclarationDocument
from auto.models.transit_declaration_document import TransitDeclarationDocument
from auto.models.transport_invoice_document import TransportInvoiceDocument


class CarTechnicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalImage
        fields = (
            "id",
            "image"
        )


class VinSerializer(serializers.ModelSerializer):

    car = CarSerializer()
    equipment = EquipmentSerializer()
    offer = OfferSerializer()
    car_ad_images = CarTechnicalImageSerializer(many=True)

    class Meta:
        model = Vin
        fields = [
            'id',
            'vin_code',
            'invoice',
            'packing_list',
            'CMR',
            'car',
            'offer',
            'equipment',
            'customs_inspection_report',
            'seller_proxy_to_broker',
            'handover_act',
            'contract',
            'status',
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
            "car_ad_images"
        ]


class CreateVinSerializer(serializers.ModelSerializer):
    car_id = serializers.UUIDField()
    equipment_id = serializers.UUIDField()
    offer_id = serializers.UUIDField()
    vin_code = serializers.CharField()
    # contract = serializers.FileField()
    # car_ad_images = serializers.ListField(
    #     child=serializers.FileField(),
    #     required=False,
    #     write_only=True
    # )

    class Meta:
        model = Vin
        fields = [
            'id',
            'vin_code',
            # 'invoice',
            # 'packing_list',
            # 'CMR',
            'car_id',
            'offer_id',
            'equipment_id',
            # 'customs_inspection_report',
            # 'seller_proxy_to_broker',
            # 'handover_act',
            # 'contract',
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
            # "car_ad_images"
        ]

    def create(self, validated_data):
        data = {}
        temp = set()
        # car_ad_images = validated_data.pop("car_ad_images", [])

        for k, v in validated_data.items():
            if isinstance(v, InMemoryUploadedFile):
                temp.add((k, v))
                continue
            data[k] = v

        vin = Vin.objects.create(**data)

        # for image in car_ad_images:
        #     TechnicalImage.objects.create(vin=vin, image=image)
        return vin


class UpdateVinSerializer(serializers.ModelSerializer):
    offer_id = serializers.UUIDField(required=False)
    vin_code = serializers.CharField()
    contract = serializers.FileField(required=False)
    # car_ad_images = serializers.ListField(child=serializers.FileField(), required=False, write_only=True)

    class Meta:
        model = Vin
        fields = [
            "offer_id",
            "vin_code",
            "contract",
            # "car_ad_images"
        ]

    def update(self, instance, validated_data):
        offer_id = validated_data.pop("offer_id", None)
        try:
            offer = Offer.objects.get(id=offer_id)
        except Offer.DoesNotExist:
            pass
        else:
            instance.offer = offer

        # if car_ad_images := validated_data.pop("car_ad_images", None):
        #     instance.car_ad_images.all().delete()
        #     for image in car_ad_images:
        #         TechnicalImage.objects.create(vin=instance, image=image)
        validated_data["status"] = StatusChoices.NEEDS_MODERATION
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class VinImagesMixin:
    image_cls = TechnicalImage
    relation_field = "vin"


class CreateVinImagesSerializer(VinImagesMixin, AbstractCreateImageSerializer):
    pass


class DeleteVinImagesSerializer(VinImagesMixin, AbstractDeleteImageSerializer):
    pass


class CreateVinDocumentsSerializer(serializers.Serializer):
    doc_type = serializers.ChoiceField(choices=DocTypeEnum.choices)
    files = serializers.ListField(child=serializers.FileField())

    class Meta:
        fields = [
            "doc_type",
            "files"
        ]
    def save(self, **kwargs):
        doc_type = self.validated_data.pop("doc_type")
        files = self.validated_data.get("files")
        if doc_type == DocTypeEnum.TRANSIT_DECLARATION_DOCUMENTS:
            updated_files_data = [
                TransitDeclarationDocument(
                    **{"vin": self.instance, "document": file}
                )
                for file in files
            ]
            TransitDeclarationDocument.objects.bulk_create(updated_files_data)
        elif doc_type == DocTypeEnum.PRODUCT_DECLARATION_DOCUMENTS:
            updated_files_data = [
                ProductDeclarationDocument(
                    **{"vin": self.instance, "file": file}
                )
                for file in files
            ]
            ProductDeclarationDocument.objects.bulk_create(updated_files_data)
        elif doc_type == DocTypeEnum.TRANSPORT_INVOICE_DOCUMENTS:
            updated_files_data = [
                TransportInvoiceDocument(
                    **{"vin": self.instance, "file": file}
                )
                for file in files
            ]
            TransportInvoiceDocument.objects.bulk_create(updated_files_data)
        else:
            setattr(self.instance, doc_type, files[0])
            self.instance.save()


class DocumentSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.UUIDField(), required=False)
    doc_type = serializers.ChoiceField(choices=DocTypeEnum.choices)


class DeleteDocumentsSerializer(serializers.Serializer):
    documents = DocumentSerializer(many=True)

    def save(self, **kwargs):
        for doc in self.validated_data.get("documents"):
            doc_type = doc.get("doc_type")
            multiple_docs_field = [
                DocTypeEnum.TRANSIT_DECLARATION_DOCUMENTS,
                DocTypeEnum.PRODUCT_DECLARATION_DOCUMENTS,
                DocTypeEnum.TRANSPORT_INVOICE_DOCUMENTS
            ]
            field = getattr(self.instance, doc_type)
            if doc_type in multiple_docs_field:
                field.filter(id__in=doc.get("ids")).delete()
            else:
                field.delete()
        return self.instance.save()

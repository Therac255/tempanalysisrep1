from uuid import UUID

from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.api.viewsets import ResponseWithRetrieveSerializerMixin
from auto.api.filters.car import CarBrandFilter, CarModelFilter
from auto.api.filters.references import EquipmentFilter
from auto.api.serializers.car_reference import (
    BodyTypeSerializer,
    BrandCarModelSerializer,
    BrandModelSerializer,
    CarBrandSerializer,
    CarColorSerializer,
    CarModelSerializer,
    CountrySerializer,
    CreateCarBrandModel,
    CreateCarModelSerializer,
    DriveSerializer,
    EngineTypeSerializer,
    EngineVolumeSerializer,
    TransmissionSerializer,
)
from auto.api.serializers.equipment import CreateEquipmentSerializer, EquipmentSerializer
from auto.models import (
    BodyType,
    CarBrand,
    CarColor,
    CarModel,
    Country,
    Drive,
    EngineType,
    EngineVolume,
    Equipment,
    Transmission,
)
from common.common import paginate_queryset


class DriveViewSet(GenericViewSet, ListModelMixin):
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer


class CountryViewSet(GenericViewSet, ListModelMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class TransmissionViewSet(GenericViewSet, ListModelMixin):
    queryset = Transmission.objects.all()
    serializer_class = TransmissionSerializer


class EngineVolumeViewSet(GenericViewSet, ListModelMixin):
    queryset = EngineVolume.objects.all()
    serializer_class = EngineVolumeSerializer


class EngineTypeViewSet(GenericViewSet, ListModelMixin):
    queryset = EngineType.objects.all()
    serializer_class = EngineTypeSerializer


class CarColorViewSet(GenericViewSet, ListModelMixin):
    queryset = CarColor.objects.all()
    serializer_class = CarColorSerializer


class BodyTypeViewSet(GenericViewSet, ListModelMixin):
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer


class CarModelViewSet(
    ResponseWithRetrieveSerializerMixin,
    CreateModelMixin,
    GenericViewSet,
    ListModelMixin
):
    queryset = CarModel.objects.all()
    serializer_class = BrandCarModelSerializer

    serializer_action_classes = {
        "create": CreateCarModelSerializer
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarModelFilter

    @extend_schema(responses={200: CarModelSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='(?P<brand_id>[^/.]+)')
    def get_all_models_by_brand_id(self, request, *args, brand_id: UUID, **kwargs):
        """
        Get list of models by brand id
        """
        queryset = self.get_queryset().filter(
            brand_id=brand_id,
            is_popular=True
        )
        return paginate_queryset(self, queryset)


class CarBrandViewSet(
    ResponseWithRetrieveSerializerMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet
):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    filter_backends = [DjangoFilterBackend]
    serializer_action_classes = {
        "create": CreateCarBrandModel,
        "get_car_model": BrandModelSerializer
    }

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by('name')
        return super().list(request, *args, **kwargs)

    @property
    def filterset_class(self):
        if self.action == "get_car_model":
            return None
        return CarBrandFilter

    @extend_schema(responses=CarBrandSerializer(many=True))
    @action(methods=["get"], detail=True, url_path="get-models")
    def get_car_model(self, request, pk: UUID):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return Response(data=serializer.data)


class CarEquipmentViewSet(
    CreateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    GenericViewSet
):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EquipmentFilter

    serializer_action_classes = {
        "create": CreateEquipmentSerializer
    }

    @extend_schema(responses={200: EquipmentSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='by-car-id/(?P<car_id>[^/.]+)')
    def get_all_equipment_by_car_id(self, request, *args, car_id: UUID, **kwargs):
        """
        Get list of equipment by car id
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                car_id=car_id
            ).order_by().distinct()
        )

        return paginate_queryset(self, queryset)

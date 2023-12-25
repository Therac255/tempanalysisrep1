from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app.api.viewsets import ResponseWithRetrieveSerializerMixin
from auto.api.filters.car import CarFilter
from auto.api.serializers.car import CarSerializer, CreateCarSerializer
from auto.enum import StatusChoices
from auto.models import Car
from common.common import paginate_queryset


class CarViewSet(
    mixins.CreateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    viewsets.GenericViewSet
):
    """
    The CarViewSet class is a viewset for the Car model.
    It provides endpoints for retrieving all cars and retrieving a specific car by its ID.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    serializer_action_classes = {
        "create": CreateCarSerializer
    }

    @extend_schema(responses={200: CarSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='all')
    def get_all_cars(self, request):
        """
        Returns a list of all cars.
        """
        queryset = self.filter_queryset(
            self.get_queryset()
            .order_by().distinct()
        )
        return paginate_queryset(self, queryset)

    @extend_schema(responses={200: CarSerializer})
    @action(detail=True, methods=['get'], url_path='detail')
    def get_car_by_id(self, request, pk: UUID):
        """
        Return a car detail.
        """
        car = get_object_or_404(Car, pk=pk)
        serializer = self.get_serializer(car)
        return Response(serializer.data)

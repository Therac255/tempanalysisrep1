from django.urls import include, path
from rest_framework.routers import DefaultRouter

from auto.api.viewsets.car import CarViewSet
from auto.api.viewsets.car_reference import (
    BodyTypeViewSet,
    CarBrandViewSet,
    CarColorViewSet,
    CarEquipmentViewSet,
    CarModelViewSet,
    CountryViewSet,
    DriveViewSet,
    EngineTypeViewSet,
    EngineVolumeViewSet,
    TransmissionViewSet,
)
from auto.api.viewsets.offer import OfferViewSet
from auto.api.viewsets.vin import VinViewSet
from auto.autocomplete import OfferModelAutocomplete, VinModelAutocomplete

router = DefaultRouter()
router.register(r'car', CarViewSet, basename='car')
router.register(r'offer', OfferViewSet, basename='offer')
router.register(r'drive', DriveViewSet, basename='drive')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'transmission', TransmissionViewSet, basename='transmission')
router.register(r'engine-volume', EngineVolumeViewSet, basename='engine-volume')
router.register(r'engine-type', EngineTypeViewSet, basename='engine-type')
router.register(r'car-color', CarColorViewSet, basename='car-color')
router.register(r'body-type', BodyTypeViewSet, basename='body-type')
router.register(r'car-model', CarModelViewSet, basename='car-model')
router.register(r'car-brand', CarBrandViewSet, basename='car-brand')
router.register(r'car-equipment', CarEquipmentViewSet, basename='car-equipment')
router.register(r'vin', VinViewSet, basename='vin')


app_name = 'auto'

urlpatterns = [
    path('car-equipment-autocomplete/', OfferModelAutocomplete.as_view(), name='offer_equipment_autocomplete'),
    path('vin-offer-autocomplete/', VinModelAutocomplete.as_view(), name='vin_offer_autocomplete'),
    path('', include(router.urls)),
]

from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, request
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app.api.viewsets import ResponseWithRetrieveSerializerMixin
from auto.api.filters.offer import OfferFilter
from auto.api.serializers.offer import (
    CreateOfferSerializer,
    OfferSerializer,
    OfferShortInfo,
    UpdateOfferSerializer,
    CreateOfferImagesSerializer,
    DeleteOfferImagesSerializer
)
from auto.api.permissions.offers import OfferPermission
from auto.enum import StatusChoices, ModerationStates
from auto.models import Offer
from auto.models.vin import Vin

from common.common import paginate_queryset

from seller.api.permissions import SellerPermission


class OfferViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    A view set that provides the standard actions for `Offer` model
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter
    permission_classes = [OfferPermission, SellerPermission]

    serializer_action_classes = {
        "create": CreateOfferSerializer,
        "update": UpdateOfferSerializer,
        "partial_update": UpdateOfferSerializer,
        "get_short_info": OfferShortInfo,
        "upload_images": CreateOfferImagesSerializer,
        "delete_images": DeleteOfferImagesSerializer
    }

    @extend_schema(responses={200: OfferSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='all')
    def get_all_offers(self, request):
        """
        Returns a list of all offers.
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                # car__vin_car__status=StatusChoices.MODERATED
            )
        )
        return paginate_queryset(self, queryset)

    @extend_schema(responses={200: OfferSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='by-car-id/(?P<car_id>[^/.]+)')
    def get_offers_by_car_id(self, request, car_id: UUID):
        """
        Return offers by car id.
        """
        offers = self.filter_queryset(
            self.get_queryset().filter(
                car=car_id
            ).order_by()
        )
        offers_ids = (
            Vin.objects.filter(
                offer__in=offers,
                status=StatusChoices.MODERATED
            )
            .values_list("offer__id")
        )
        queryset = offers.filter(id__in=offers_ids, state=ModerationStates.APPROVED)
        if not queryset:
            raise NotFound("No Offers are associated with this Car ID or filter")
        return paginate_queryset(self, queryset)

    @extend_schema(responses={200: OfferSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='by-seller-id/(?P<seller_id>[^/.]+)')
    def get_offers_by_seller_id(self, request: request.Request, seller_id: UUID):
        """
        Return offers by seller id.
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                seller=seller_id,
                vin_offer__status__in=[StatusChoices.MODERATED],
                state=ModerationStates.APPROVED
            ).order_by().distinct()
        )
        if not queryset:
            raise NotFound("No Offers are associated with this Seller ID or filter")
        return paginate_queryset(self, queryset)

    @extend_schema(responses={200: OfferSerializer()})
    @action(detail=True, methods=['get'], url_path='detail')
    def get_offer_by_id(self, request, pk: UUID):
        """
        Return an offer detail.
        """
        offer = get_object_or_404(Offer, pk=pk)
        serializer = self.get_serializer(offer)
        return Response(serializer.data)

    @extend_schema(request=CreateOfferSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(request=UpdateOfferSerializer)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return super().update(request, *args, **kwargs)

    @action(methods=["get"], detail=False, url_path="short-info")
    def get_short_info(self, request):
        qs = self.get_queryset().filter(
            seller=request.user.seller,
            car__vin_car__status__in=[StatusChoices.MODERATED, StatusChoices.NEEDS_MODERATION]
        ).distinct("car", "equipment")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=True, url_path="upload-images")
    def upload_images(self, request, pk: UUID):
        obj = self.get_object()
        serializer = self.get_serializer(
            instance=obj,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.response(obj, status=201)

    @action(methods=["put"], detail=True, url_path="delete-images")
    def delete_images(self, request, pk: UUID):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

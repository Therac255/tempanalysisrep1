from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.api.viewsets import ResponseWithRetrieveSerializerMixin
from auto.api.filters.vin import VinFilter
from auto.api.permissions.vin import VINPermission
from auto.api.serializers.vin import (
    CreateVinSerializer,
    UpdateVinSerializer,
    VinSerializer,
    CreateVinImagesSerializer,
    DeleteVinImagesSerializer,
    CreateVinDocumentsSerializer,
    DeleteDocumentsSerializer
)
from auto.models import Vin
from common.common import paginate_queryset


class VinViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    ResponseWithRetrieveSerializerMixin,
    GenericViewSet,
):
    """
    View set to handle Vin objects
    """
    queryset = Vin.objects.all()
    serializer_class = VinSerializer
    filterset_class = VinFilter
    filter_backends = [DjangoFilterBackend]
    serializer_action_classes = {
        "create": CreateVinSerializer,
        "partial_update": UpdateVinSerializer,
        "update": UpdateVinSerializer,
        "upload_images": CreateVinImagesSerializer,
        "delete_images": DeleteVinImagesSerializer,
        "upload_documents": CreateVinDocumentsSerializer,
        "delete_documents": DeleteDocumentsSerializer
    }

    def get_permissions(self):
        if self.request.method.lower() in ["patch", "delete", "post", "put"]:
            return [VINPermission()]
        return super().get_permissions()

    @extend_schema(responses={200: VinSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='seller/(?P<seller_id>[^/.]+)')
    def get_vins_by_seller(self, request, seller_id: UUID):
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                offer__seller_id=seller_id
            )
        )
        return paginate_queryset(self, queryset)

    @extend_schema(
        request=UpdateVinSerializer,
        responses={200: VinSerializer(many=False)}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(responses={200: VinSerializer(many=True)})
    @action(detail=True, methods=['get'])
    def get_vin_by_id(self, request, pk=None):
        queryset = self.filter_queryset(
            self.get_queryset().get(
                id=pk
            )
        )
        return Response(VinSerializer(queryset, many=True).data)
    
    @action(methods=["post"], detail=True, url_path="upload-images")
    def upload_images(self, request, pk: UUID):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.response(instance=obj, status=201)
    
    @action(methods=["put"], detail=True, url_path="delete-images")
    def delete_images(self, request, pk: UUID):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

    @action(methods=["post"], detail=True, url_path="upload-documents")
    def upload_documents(self, request, pk: UUID):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.response(instance=obj, status=201)

    @action(methods=["put"], detail=True, url_path="delete-documents")
    def delete_documents(self, request, pk: UUID):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

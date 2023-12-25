from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets

from app.api.viewsets import ResponseWithRetrieveSerializerMixin
from buyer.api.serializers.buyer import (
    BuyerDocumentUploadSerializer,
    BuyerPersonalInfoUpdateSerializer,
    BuyerSerializer,
)
from buyer.models import Buyer


class BuyerView(
    ResponseWithRetrieveSerializerMixin,
    viewsets.GenericViewSet
):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    serializer_action_classes = {
        "retrieve": BuyerSerializer,
        "partial_update": BuyerPersonalInfoUpdateSerializer,
        "upload_doc": BuyerDocumentUploadSerializer
    }
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk: UUID, *args, **kwargs):
        obj = self.get_object()
        return self.response(instance=obj, status=200)

    @extend_schema(request=BuyerPersonalInfoUpdateSerializer)
    def partial_update(self, request, pk: UUID, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return self.response(instance=instance, status=200)

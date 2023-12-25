from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from auto.enum import StatusChoices
from auto.models.vin import Vin


class OfferPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if obj.seller != request.user.seller:
            return False

        vins = Vin.objects.filter(car=obj.car, offer=obj)
        if obj.car.vin_car.filter(
            id__in=vins,
            status__in=[
                StatusChoices.IN_TRANSIT,
                StatusChoices.PAID,
                StatusChoices.READY,
                StatusChoices.RESERVED
            ]
        ):
            self.message = _("У предложения есть покупатель")
            return False
        return True
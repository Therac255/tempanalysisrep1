from django.utils.translation import gettext_lazy as _

from rest_framework import permissions

from auto.enum import StatusChoices


class VINPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.status in [
            StatusChoices.READY,
            StatusChoices.PAID,
            StatusChoices.RESERVED,
            StatusChoices.IN_TRANSIT
        ]:
            self.message = _("У предложения есть покупатель")
            return False
        return super().has_object_permission(request, view, obj)

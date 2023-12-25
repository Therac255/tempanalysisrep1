from django_filters.rest_framework import filterset as filters

from auto.enum import StatusChoices


class EquipmentFilter(filters.FilterSet):
    is_all = filters.BooleanFilter(method="filter_status", required=True)

    def filter_status(self, qs, name, value):
        if value:
            return qs
        return qs.filter(equipment_offers__vin_offer__status=StatusChoices.MODERATED)

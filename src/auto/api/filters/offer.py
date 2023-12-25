from django.db.models import Q
from django_filters import rest_framework as filters
# from auto.enum import StatusChoices

from auto.models import Offer


class OfferFilter(filters.FilterSet):
    """
    Class to filter Offer objects
    """
    brand = filters.CharFilter(field_name="car__brand__name")
    model = filters.CharFilter(field_name="car__model__name")
    body_type = filters.CharFilter(field_name="car__body_type__name")
    color = filters.CharFilter(field_name="car__color__name")
    engine_type = filters.CharFilter(field_name="car__engine_type__name")
    engine_volume = filters.CharFilter(field_name="car__engine_volume__volume")
    transmission_type = filters.CharFilter(field_name="car__transmission_type__name")
    drive_type = filters.CharFilter(field_name="car__drive_type__name")
    assembly_country = filters.CharFilter(field_name="car__assembly_country__name")
    equipment = filters.CharFilter(field_name="equipment__name", lookup_expr='exact')
    search = filters.CharFilter(method='filter_search', field_name='search')
    # is_all = filters.BooleanFilter(method='filter_is_all')

    class Meta:
        model = Offer
        fields = {
            'price': ['exact', 'lte', 'gte'],
            'discounted_price': ['exact', 'lte', 'gte'],
        }

    @staticmethod
    def filter_search(queryset, name, value):
        """
        This function is called when a search is triggered. It will look in 'brand', 'model' and any other field
        you want to search in.
        """
        return queryset.filter(
            Q(car__brand__name__icontains=value) |
            Q(car__model__name__icontains=value) |
            Q(car__body_type__name__icontains=value) |
            Q(car__color__name__icontains=value)
        )

    # def filter_is_all(self, qs, name, value):
    #     if not value:
    #         return qs.filter(vin_offer__status__in=[StatusChoices.MODERATED])
    #     return qs

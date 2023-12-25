from django.db.models import Q
from django_filters import rest_framework as filters

from auto.models import Vin


class VinFilter(filters.FilterSet):
    vin_status = filters.CharFilter(field_name="status")
    offer_status = filters.CharFilter(field_name="offer__state")
    order_price = filters.OrderingFilter(
        fields=(
            ('offer__price', 'price'),
            ('offer__discounted_price', 'discounted_price'),
            ('created', 'created_vin'),
        )
    )
    search = filters.CharFilter(method='filter_search', field_name='search')
    offer_id = filters.UUIDFilter(field_name="offer_id")

    class Meta:
        model = Vin
        fields = [
            'vin_status',
            'offer_status',
        ]

    @staticmethod
    def filter_search(queryset, name, value):
        return queryset.filter(
            Q(car__brand__name__icontains=value) |
            Q(car__model__name__icontains=value) |
            Q(vin_code__icontains=value)
        )

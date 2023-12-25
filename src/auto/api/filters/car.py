from django.db.models import Case, F, FloatField, Max, Min, Q, When
from django_filters import rest_framework as filters
from auto.enum import StatusChoices

from auto.models import Car
from auto.models.car_brand import CarBrand
from auto.models.car_model import CarModel
from seller.enums import SortByEnum


class CarFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name="brand__name")
    model = filters.CharFilter(field_name="model__name")
    body_type = filters.CharFilter(field_name="body_type__name")
    color = filters.CharFilter(field_name="color__name")
    engine_type = filters.CharFilter(field_name="engine_type__name")
    engine_volume = filters.CharFilter(field_name="engine_volume__volume")
    transmission_type = filters.CharFilter(field_name="transmission_type__name")
    drive_type = filters.CharFilter(field_name="drive_type__name")
    assembly_country = filters.CharFilter(field_name="assembly_country__name")
    search = filters.CharFilter(method='filter_search', field_name='search')
    order_price = filters.ChoiceFilter(choices=SortByEnum.choices, method="get_order_price")
    min_price = filters.NumberFilter(method="filter_min_price")
    max_price = filters.NumberFilter(method="filter_max_price")
    is_all = filters.BooleanFilter(method="filter_is_all", required=True)

    # min_discounted_price = filters.NumberFilter(method="filter_min_discounted_price")
    # max_discounted_price = filters.NumberFilter(method="filter_max_discounted_price")

    class Meta:
        model = Car
        fields = [
            'brand',
            'model',
            'body_type',
            'color',
            'engine_type',
            'engine_volume',
            'transmission_type',
            'drive_type',
            'assembly_country',
            'manufacturing_year',
            'horsepower',
            'steering_side',
            'fuel_consumption',
            'acceleration',
            'length',
            'height',
            'clearance',
            'wheelbase',
            'front_track',
            'rear_track',
            'front_tire_size',
            'rear_tire_size',
            'engine_displacement',
            'num_of_cylinders',
            'front_brakes',
            'rear_brakes',
            'num_of_doors',
            'euroNCAP_rating',
        ]

    @staticmethod
    def filter_min_price(queryset, name, value):
        # return queryset.filter(car_offers__price__gte=value).order_by().distinct()
        return queryset.annotate(
            min_price=Min(
                Case(
                    When(
                        car_offers__discounted_price__gte=value, then=F('car_offers__discounted_price')),
                    default=F('car_offers__price'),
                    output_field=FloatField()
                )
            )
        ).filter(min_price__gte=value)

    @staticmethod
    def filter_max_price(queryset, name, value):
        # return queryset.filter(car_offers__price__lte=value).order_by().distinct()
        return queryset.annotate(
            max_price=Max(
                Case(
                    When(
                        car_offers__discounted_price__gte=value, then=F('car_offers__discounted_price')),
                    default=F('car_offers__price'),
                    output_field=FloatField()
                )
            )
        ).filter(max_price__lte=value)

    # @staticmethod
    # def filter_min_discounted_price(queryset, name, value):
    #     return queryset.filter(car_offers__discounted_price__gte=value).order_by().distinct()

    # @staticmethod
    # def filter_max_discounted_price(queryset, name, value):
    #     return queryset.filter(car_offers__discounted_price__lte=value).order_by().distinct()

    @staticmethod
    def filter_search(queryset, name, value):
        """
        This function is called when a search is triggered. It will look in 'brand', 'model' and any other field
        you want to search in.
        """
        return queryset.filter(
            Q(brand__name__icontains=value)
            | Q(model__name__icontains=value)
            | Q(body_type__name__icontains=value)
            | Q(color__name__icontains=value)
            | Q(engine_type__name__icontains=value)
            | Q(engine_volume__volume__icontains=value)
            | Q(transmission_type__name__icontains=value)
        )

    def get_order_price(self, qs, name, value):
        qs = qs.annotate(
            minimum_price=Min(
                Case(
                    When(
                        car_offers__discounted_price__gt=0, then=F('car_offers__discounted_price')),
                    default=F('car_offers__price'),
                    output_field=FloatField()
                )
            )
        ).order_by("minimum_price" if value == SortByEnum.ASC else "-minimum_price")
        return qs

    def filter_is_all(self, qs, name, value):
        if not value:
            return qs.filter(
                car_offers__vin_offer__status=StatusChoices.MODERATED
            )
        return qs


class NameFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    is_popular = filters.BooleanFilter()
    class Meta:
        fields = [
            "name"
        ]


class CarBrandFilter(NameFilter):
    class Meta(NameFilter.Meta):
        model = CarBrand


class CarModelFilter(NameFilter):
    class Meta(NameFilter.Meta):
        model = CarModel

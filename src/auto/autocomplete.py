from dal import autocomplete
from django.db.models import Q

from auto.models import Equipment, Offer


class OfferModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        car_id = self.forwarded.get('car')
        queryset = Equipment.objects.none()
        if car_id:
            queryset = Equipment.objects.filter(car_id=car_id)
        if self.q:
            queryset = queryset.filter(name__istartswith=self.q)
        return queryset


class VinModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        car = self.forwarded.get('car')
        equipment = self.forwarded.get('equipment')
        filters = Q(car_id=car, equipment_id=equipment)
        if self.q:
            query = self.q.split()
            personal_info_filters = Q()
            field_names = ['first_name', 'last_name', 'patronymic']
            for field in field_names:
                if query:
                    filter_condition = {f'seller__user__personal_info__{field}__icontains': query.pop(0)}
                    personal_info_filters |= Q(**filter_condition)
            filters &= personal_info_filters
        return Offer.objects.filter(filters)

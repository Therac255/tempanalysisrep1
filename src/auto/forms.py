from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError

from auto.models import Offer, Vin


class OfferForm(forms.ModelForm):
    def clean_equipment(self):
        equipment = self.cleaned_data.get('equipment')
        car = self.cleaned_data.get('car')
        if equipment.car != car:
            raise ValidationError('This equipment for car don\'t exist\'s')
        return equipment

    class Meta:
        model = Offer
        fields = '__all__'
        widgets = {
            'equipment': autocomplete.ModelSelect2(url='api_v1:auto:offer_equipment_autocomplete', forward=['car'])
        }


class VinForm(forms.ModelForm):
    def clean_offer(self):
        offer = self.cleaned_data.get('offer')
        car = self.cleaned_data.get('car')
        if offer.car != car:
            raise ValidationError('This offer for car don\'t exist\'s')
        return offer

    class Meta:
        model = Vin
        fields = '__all__'
        widgets = {
            'equipment': autocomplete.ModelSelect2(url='api_v1:auto:offer_equipment_autocomplete', forward=['car']),
            'offer': autocomplete.ModelSelect2(url='api_v1:auto:vin_offer_autocomplete', forward=['car', 'equipment']),
        }

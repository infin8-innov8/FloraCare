from django import forms
from .models import BloodInventory, BloodRequest


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['requester_name', 'phone', 'blood_group', 'city', 'urgency']
        widgets = {
            'requester_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
        }


class BloodInventoryForm(forms.ModelForm):
    class Meta:
        model = BloodInventory
        fields = ['blood_group', 'location_name', 'city', 'latitude', 'longitude', 'units_available']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'location_name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'units_available': forms.NumberInput(attrs={'class': 'form-control'}),
        }
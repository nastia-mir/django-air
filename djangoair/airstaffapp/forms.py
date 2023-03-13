from django.forms import ModelForm, Select, SelectMultiple, NumberInput, DateInput, TextInput

from accounts.models import Staff
from airstaffapp.models import Flight, FlightDate, LunchOptions, LuggageOptions


class StaffRoleEditForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['role']

        widgets = {
            'role': Select(attrs={'class': 'form-control'})
        }


class LunchOptionsForm(ModelForm):
    class Meta:
        model = LunchOptions
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
        }


class LuggageOptionsForm(ModelForm):
    class Meta:
        model = LuggageOptions
        fields = '__all__'

        widgets = {
            'quantity': Select(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
        }


class DateForm(ModelForm):
    class Meta:
        model = FlightDate
        fields = ['date']

        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
        }


class FlightCreationForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['destination', 'passengers', 'ticket_price', 'lunch', 'luggage', 'extra_luggage_price']

        widgets = {
            'destination': Select(attrs={'class': 'form-control'}),
            'passengers': NumberInput(attrs={'class': 'form-control'}),
            'ticket_price': NumberInput(attrs={'class': 'form-control'}),
            'lunch': SelectMultiple(attrs={'class': 'form-control'}),
            'luggage': SelectMultiple(attrs={'class': 'form-control'}),
            'extra_luggage_price': NumberInput(attrs={'class': 'form-control'}),
        }
from django.forms import ModelForm
from django.forms.widgets import DateInput

from accounts.models import Staff
from airstaffapp.models import Flight, LunchOptions, LuggageOptions


class StaffRoleEditForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['role']


class LunchOptionsForm(ModelForm):
    class Meta:
        model = LunchOptions
        fields = '__all__'


class LuggageOptionsForm(ModelForm):
    class Meta:
        model = LuggageOptions
        fields = '__all__'


class FlightCreationForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['destination', 'date', 'passengers', 'ticket_price', 'lunch', 'luggage']

        widget = {
            'date': DateInput(attrs={'type': 'date'})
        }
from django.forms import ModelForm

from accounts.models import Staff
from airstaffapp.models import Flight, FlightDate, LunchOptions, LuggageOptions


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


class DateForm(ModelForm):
    class Meta:
        model = FlightDate
        fields = ['date']


class FlightCreationForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['destination', 'passengers', 'ticket_price', 'lunch', 'luggage', 'extra_luggage_price']
from django.forms import ModelForm
from django.forms.widgets import DateInput
from accounts.models import Staff
from airstaffapp.models import Flight, FlightOptions


class StaffRoleEditForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['role']


class FlightOptionsForm(ModelForm):
    class Meta:
        model = FlightOptions
        fields = '__all__'


class FlightCreationForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['destination', 'date', 'passengers', 'price']

        widget = {
            'date': DateInput(attrs={'type': 'date'})
        }






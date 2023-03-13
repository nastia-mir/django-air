from django.forms import ModelForm, TextInput

from airstaffapp.models import Flight

from airuserapp.models import CheckIn


class TicketForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['destination', 'date', 'passengers']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].queryset = Flight.objects.none()

        if 'destination' in self.data:
            try:
                destination = int(self.data.get('destination'))
                self.fields['date'].queryset = Flight.objects.filter(destination=destination).order_by('date')
            except (ValueError, TypeError):
                pass


class CheckInForm(ModelForm):
    class Meta:
        model = CheckIn
        fields = ['passenger_first_name', 'passenger_last_name', 'extra_luggage']

        widgets = {
            'passenger_first_name': TextInput(attrs={'class': 'form-control'}),
            'passenger_last_name': TextInput(attrs={'class': 'form-control'}),
        }


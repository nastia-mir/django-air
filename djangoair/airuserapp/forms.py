from django.forms import ModelForm, TextInput, Select, NumberInput

from airstaffapp.models import Flight

from airuserapp.models import PassengerFullName, ExtraLuggageTicket


class TicketForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['destination', 'date', 'passengers']

        widgets = {
            'destination': Select(attrs={'class': 'form-control'}),
            'date': Select(attrs={'class': 'form-control'}),
            'passengers': NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].queryset = Flight.objects.none()

        if 'destination' in self.data:
            try:
                destination = int(self.data.get('destination'))
                self.fields['date'].queryset = Flight.objects.filter(destination=destination).order_by('date')
            except (ValueError, TypeError):
                pass


class PassengerFullNameForm(ModelForm):
    class Meta:
        model = PassengerFullName
        fields = ['passenger_first_name', 'passenger_last_name']

        widgets = {
            'passenger_first_name': TextInput(attrs={'class': 'form-control'}),
            'passenger_last_name': TextInput(attrs={'class': 'form-control'}),
        }


class ExtraLuggageTicketForm(ModelForm):
    class Meta:
        model = ExtraLuggageTicket
        fields = ['amount']

        widgets = {
            'amount': NumberInput(attrs={'class': 'form-control'})
        }

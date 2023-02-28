from django.forms import ModelForm, ChoiceField, Form, CharField

from airstaffapp.models import Flight

from airuserapp.models import PassengerName


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

    widgets = {'date': ChoiceField()}


class PassengerNameForm(ModelForm):
    class Meta:
        model = PassengerName
        fields = ['first_name', 'last_name']


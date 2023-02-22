from django.forms import ModelForm, Form, CharField, DateField, ChoiceField

from airstaffapp.models import Flight
from airuserapp.models import Ticket


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
        # elif self.instance.pk:
        #    self.fields['data'].queryset = self.instance.flight.city_set.order_by('date')

    widgets = {'date': ChoiceField()}


class TicketOptionsForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['lunch', 'luggage']

from django.db import models

from airstaffapp.models import Flight, LunchOptions, LuggageOptions
from accounts.models import Passenger


class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='passenger', null=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flight')
    tickets_quantity = models.IntegerField(blank=False, null=False)
    lunch = models.ForeignKey(LunchOptions, on_delete=models.CASCADE, related_name='lunch', null=True)
    luggage = models.ForeignKey(LuggageOptions, on_delete=models.CASCADE, related_name='luggage', null=True)

    objects = models.Manager()

    def __str__(self):
        return '{}, {} tickets to {}'.format(self.passenger, self.tickets_quantity, self.flight)

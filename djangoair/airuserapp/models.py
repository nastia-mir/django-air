from django.db import models

from airstaffapp.models import Flight, LunchOptions, LuggageOptions
from accounts.models import Passenger


class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='passenger', null=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flight')
    tickets_quantity = models.IntegerField(blank=False, null=False)
    lunch = models.ForeignKey(LunchOptions, on_delete=models.CASCADE, related_name='lunch', null=True)
    luggage = models.ForeignKey(LuggageOptions, on_delete=models.CASCADE, related_name='luggage', null=True)

    check_in = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return '{}, {} tickets to {}'.format(self.passenger, self.tickets_quantity, self.flight)


class CheckIn(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket')
    passenger_first_name = models.CharField(max_length=150, null=False, blank=False)
    passenger_last_name = models.CharField(max_length=150, null=False, blank=False)
    extra_luggage = models.IntegerField(default=0)
    status_choices = (
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    )
    status = models.CharField(max_length=100, choices=status_choices, blank=True)

    objects = models.Manager()

    def __str__(self):
        return '{}, status: {}'.format(self.ticket, self.get_status_display())


class BoardingPass(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='boarding_pass')
    passenger_first_name = models.CharField(max_length=150, null=False, blank=False)
    passenger_last_name = models.CharField(max_length=150, null=False, blank=False)
    code = models.CharField(max_length=10, blank=False, null=False)

    objects = models.Manager()

    def __str__(self):
        return '{}, {}'.format(self.code, self.passenger)

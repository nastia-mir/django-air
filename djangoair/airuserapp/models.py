from enum import Enum

from django.db import models

from airstaffapp.models import Flight, LunchOptions, LuggageOptions
from accounts.models import Passenger


class StatusOptions(Enum):
    no_checkin = 'no_checkin'
    editing = 'editing'
    waiting_for_approval = 'waiting_for_approval'
    completed = 'completed'
    not_registered = 'not_registered'
    in_progress = 'in_progress'


class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='passenger', null=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flight')
    tickets_quantity = models.IntegerField(blank=False, null=False)
    lunch = models.ForeignKey(LunchOptions, on_delete=models.CASCADE, related_name='lunch', null=True)
    luggage = models.ForeignKey(LuggageOptions, on_delete=models.CASCADE, related_name='luggage', null=True)

    checkin_options = (
        (StatusOptions.no_checkin.value, 'No check-in'),
        (StatusOptions.editing.value, 'Editing'),  # check-in requests not for all passengers from ticket
        (StatusOptions.waiting_for_approval.value, 'Waiting for approval'),
        (StatusOptions.completed.value, 'Completed')
    )
    check_in = models.CharField(max_length=150, choices=checkin_options, default=StatusOptions.no_checkin.value)

    gate_registration_options = (
        (StatusOptions.not_registered.value, 'Not registered'),
        (StatusOptions.waiting_for_approval.value, 'Waiting for approval'),
        (StatusOptions.completed.value, 'Completed')
    )

    gate_registration = models.CharField(max_length=150, choices=gate_registration_options, default=StatusOptions.not_registered.value)

    objects = models.Manager()

    def __str__(self):
        return '{} tickets to {}'.format(self.tickets_quantity, self.flight)


class CheckIn(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket')
    passenger_first_name = models.CharField(max_length=150, null=False, blank=False)
    passenger_last_name = models.CharField(max_length=150, null=False, blank=False)
    extra_luggage = models.IntegerField(default=0)
    status_choices = (
        (StatusOptions.in_progress.value, 'In progress'),
        (StatusOptions.completed.value, 'Completed')
    )
    status = models.CharField(max_length=100, choices=status_choices, default=StatusOptions.in_progress.value)

    objects = models.Manager()

    def __str__(self):
        return '{} {}, status: {}'.format(self.passenger_first_name, self.passenger_last_name, self.get_status_display())


class BoardingPass(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='boarding_pass')
    passenger_first_name = models.CharField(max_length=150, null=False, blank=False)
    passenger_last_name = models.CharField(max_length=150, null=False, blank=False)
    extra_luggage = models.IntegerField(default=0)
    code = models.CharField(max_length=10, blank=False, null=False)

    status_choices = (
        (StatusOptions.not_registered.value, 'Not registered'),
        (StatusOptions.in_progress.value, 'In progress'),
        (StatusOptions.completed.value, 'Completed')
    )
    status = models.CharField(max_length=100, choices=status_choices, default=StatusOptions.not_registered.value)

    objects = models.Manager()

    def __str__(self):
        return '{}, {} {}'.format(self.code, self.passenger_first_name, self.passenger_last_name)

from enum import Enum

from django.db import models

from airstaffapp.models import Flight, LunchOptions, LuggageOptions
from accounts.models import Passenger


class StatusOptions(Enum):
    no_checkin = 'no_checkin'
    editing = 'editing'
    waiting_for_extra_payment = 'waiting_for_extra_payment'
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

    is_paid = models.BooleanField(default=False)

    checkin_options = (
        (StatusOptions.no_checkin.value, 'No check-in'),
        (StatusOptions.editing.value, 'Editing'),  # check-in requests not for all passengers from ticket
        (StatusOptions.waiting_for_extra_payment.value, 'Waiting for extra payment'),
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


class PassengerFullName(models.Model):
    passenger_first_name = models.CharField(max_length=150, null=False, blank=False)
    passenger_last_name = models.CharField(max_length=150, null=False, blank=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket')

    objects = models.Manager()

    def __str__(self):
        return '{} {}'.format(self.passenger_first_name, self.passenger_last_name)


class ExtraLuggageTicket(models.Model):
    amount = models.IntegerField(default=0)
    passenger = models.OneToOneField(PassengerFullName, on_delete=models.CASCADE, related_name='extra_luggage_ticket')
    is_paid = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return '{}, {} extra luggage'.format(self.passenger, self.amount)


class CheckIn(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_checkin')
    passenger = models.OneToOneField(PassengerFullName, on_delete=models.CASCADE, related_name='passenger_checkin',
                                     null=True, blank=True)
    extra_luggage = models.OneToOneField(ExtraLuggageTicket, on_delete=models.CASCADE, related_name='extra_luggage_checkin',
                                         null=True, blank=True)
    status_choices = (
        (StatusOptions.waiting_for_extra_payment.value, 'Waiting for extra payment'),
        (StatusOptions.in_progress.value, 'In progress'),
        (StatusOptions.completed.value, 'Completed')
    )
    status = models.CharField(max_length=100, choices=status_choices, default=StatusOptions.in_progress.value)

    objects = models.Manager()

    def __str__(self):
        return '{}, status: {}'.format(self.passenger, self.get_status_display())


class BoardingPass(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='boarding_pass')
    passenger = models.OneToOneField(PassengerFullName, on_delete=models.CASCADE, related_name='passenger')
    extra_luggage = models.OneToOneField(ExtraLuggageTicket, on_delete=models.CASCADE, related_name='extra_luggage_boarding_pass',
                                         null=True, blank=True)
    code = models.CharField(max_length=10, blank=False, null=False)

    status_choices = (
        (StatusOptions.not_registered.value, 'Not registered'),
        (StatusOptions.in_progress.value, 'In progress'),
        (StatusOptions.completed.value, 'Completed')
    )
    status = models.CharField(max_length=100, choices=status_choices, default=StatusOptions.not_registered.value)

    objects = models.Manager()

    def __str__(self):
        return '{}, {}'.format(self.code, self.passenger)


class TicketBill(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='ticket_bill')
    total_price = models.IntegerField()
    stripe_charge = models.CharField(max_length=27, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return '{} paid on {}'.format(self.ticket, self.date_created)


class ExtraLuggageBill(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_luggage_bill', null=True)
    luggage_amount = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    stripe_charge = models.CharField(max_length=27, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return '{} extra luggage paid on {}'.format(self.luggage_amount, self.date_created)

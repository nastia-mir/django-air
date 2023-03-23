import stripe

from mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import MyUser, Passenger

from airstaffapp.models import FlightDate, Flight, LunchOptions, LuggageOptions

from airuserapp.models import Ticket, CheckIn, PassengerFullName, ExtraLuggageTicket, TicketBill

from djangoairproject import settings


class TestStripePayments(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = MyUser.objects.create_user(
            email='test@gmail.com',
            password='strongpassword'
        )
        self.passenger_account = Passenger.objects.create(user=self.user)
        self.client.post(self.login_url, {'email': 'test@gmail.com',
                                          'password': 'strongpassword'})

        self.lunch = LunchOptions.objects.create(
            description='Soup',
            price=20
        )
        self.luggage = LuggageOptions.objects.create(
            quantity='0',
            price=0
        )
        self.date = FlightDate.objects.create(date='2023-03-27')
        self.flight = Flight.objects.create(
            destination='lisbon',
            date=self.date,
            passengers=60,
            ticket_price=30,
            extra_luggage_price=40
        )
        self.flight.lunch.add(self.lunch)
        self.flight.luggage.add(self.luggage)
        self.ticket = Ticket.objects.create(
            passenger=self.passenger_account,
            flight=self.flight,
            tickets_quantity=1,
            lunch=self.lunch,
            luggage=self.luggage
        )
        self.passenger_full_name = PassengerFullName.objects.create(
            passenger_first_name='John',
            passenger_last_name='Doe',
            ticket=self.ticket
        )
        self.extra_luggage = ExtraLuggageTicket.objects.create(
            amount=1,
            passenger=self.passenger_full_name
        )
        self.checkin = CheckIn.objects.create(
            ticket=self.ticket,
            passenger=self.passenger_full_name,
            extra_luggage=self.extra_luggage
        )
        self.ticket_payment_url = reverse('passengers:ticket payment', args={self.ticket.id, 30})
        self.extra_luggage_payment_url = reverse('passengers:extra luggage payment', args={self.ticket.id, 50})

        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.customer = stripe.Customer.create(
            email=self.user.email,
            source='tok_visa'
        )
        self.ticket_for_bill = Ticket.objects.create(
            passenger=self.passenger_account,
            flight=self.flight,
            tickets_quantity=1,
            lunch=self.lunch,
            luggage=self.luggage
        )
        self.ticket_charge = stripe.Charge.create(
            customer=self.customer,
            amount=3000,
            currency='usd',
            description='Django Air ticket payment',
        )
        self.ticket_bill = TicketBill.objects.create(
            ticket=self.ticket_for_bill,
            total_price=30,
            stripe_charge=self.ticket_charge.id
        )
        self.refund_url = reverse('passengers:refund', args={self.ticket_for_bill.id})
        return super().setUp()

    def test_ProcessTicketPaymentView_POST(self):
        response = self.client.post(self.ticket_payment_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('passengers:view ticket', args={self.ticket.id}))

    def test_ProcessExtraLuggagePaymentView_POST(self):
        response = self.client.post(self.extra_luggage_payment_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('passengers:view ticket', args={self.ticket.id}))

    def test_RefundView_POST(self):
        response = self.client.post(self.refund_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('passengers:view ticket', args={self.ticket_for_bill.id}))
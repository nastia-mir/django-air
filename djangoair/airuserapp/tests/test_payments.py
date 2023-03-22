import stripe

from mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import MyUser, Passenger

from airstaffapp.models import FlightDate, Flight, LunchOptions, LuggageOptions

from airuserapp.models import Ticket, CheckIn, PassengerFullName, ExtraLuggageTicket

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
            tickets_quantity=1
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
        self.refund_url = reverse('passengers:refund', args={self.ticket.id})
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return super().setUp()

    @patch('stripe.Customer.create')
    @patch('stripe.Customer.search')
    @patch('stripe.Charge.create')
    @patch('airuserapp.models.TicketBill.objects.create')
    def test_ProcessTicketPaymentView_POST(self, mock_bill_creation, mock_charge_create, mock_customer_search,
                                           mock_customer_create):
        response = self.client.post(self.ticket_payment_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('passengers:view ticket', args={self.ticket.id}))

    @patch('stripe.Customer.search')
    @patch('stripe.Charge.create')
    @patch('airuserapp.models.Ticket.objects.get')
    @patch('airuserapp.models.CheckIn.objects.filter')
    @patch('airuserapp.models.ExtraLuggageBill.objects.create')
    def test_ProcessExtraLuggagePaymentView_POST(self, mock_bill_creation, mock_checkin_filter, mock_ticket_get,
                                                 mock_charge_create, mock_customer_search):
        response = self.client.post(self.extra_luggage_payment_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('passengers:view ticket', args={self.ticket.id}))

    @patch('stripe.Refund.create')
    @patch('airuserapp.services.Charges.get_all_related_charges')
    @patch('airuserapp.models.Ticket.objects.get')
    def test_RefundView_POST(self, mock_ticket_get, mock_get_related_charges, mock_refund_create):
        response = self.client.post(self.refund_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('passengers:view ticket', args={self.ticket.id}))

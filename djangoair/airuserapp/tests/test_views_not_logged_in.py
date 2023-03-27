from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from accounts.models import MyUser, Passenger

from airstaffapp.models import FlightDate, Flight, LunchOptions, LuggageOptions

from airuserapp.models import Ticket, CheckIn


class TestTicketViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('passengers:home')
        self.tickets_url = reverse('passengers:tickets')

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
            extra_luggage_price=30
        )
        self.flight.lunch.add(self.lunch)
        self.flight.luggage.add(self.luggage)
        self.ticket_draft = Ticket.objects.create(
            flight=self.flight,
            tickets_quantity=1
        )
        self.ticket_details_url = reverse('passengers:ticket details', args={self.ticket_draft.id})
        self.ticket_booking_url = reverse('passengers:ticket booking', args={self.ticket_draft.id})
        self.view_ticket_url = reverse('passengers:view ticket', args={self.ticket_draft.id})

        self.ticket_details_valid_data = {
            'lunch': self.lunch,
            'luggage': self.luggage
        }

        self.booking_valid_email = {'email': 'test@gmail.com'}
        self.booking_invalid_email = {'email': 'notemail'}
        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_passenger.html')

    def test_ticket_search_GET(self):
        response = self.client.get(self.tickets_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets.html')

    def test_ticket_details_GET(self):
        response = self.client.get(self.ticket_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket_details.html')

    def test_ticket_details_POST_valid_data(self):
        response = self.client.post(self.ticket_details_url, self.ticket_details_valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.ticket_booking_url)

    def test_ticket_booking_GET(self):
        response = self.client.get(self.ticket_booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket_booking.html')

    def test_ticket_booking_POST_valid_email(self):
        response = self.client.post(self.ticket_booking_url, self.booking_valid_email)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_ticket_booking_POST_invalid_email(self):
        response = self.client.post(self.ticket_booking_url, self.booking_invalid_email)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.ticket_booking_url)
        messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("Please enter valid email." in messages[0].message)

    def test_view_ticket_GET(self):
        response = self.client.get(self.view_ticket_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/passengers/view_ticket/8/')


class TestCheckinGateViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = MyUser.objects.create_user(
            email='test@gmail.com',
            password='strongpassword'
        )
        self.passenger = Passenger.objects.create(user=self.user)

        self.date = FlightDate.objects.create(date='2023-03-27')
        self.flight = Flight.objects.create(
            destination='lisbon',
            date=self.date,
            passengers=60,
            ticket_price=30,
            extra_luggage_price=30
        )
        self.ticket_no_checkin = Ticket.objects.create(
            passenger=self.passenger,
            flight=self.flight,
            tickets_quantity=1
        )
        self.ticket_checkin = Ticket.objects.create(
            passenger=self.passenger,
            flight=self.flight,
            tickets_quantity=1,
            check_in='completed'
        )

        self.checkin = CheckIn.objects.create(
            ticket=self.ticket_no_checkin,
            passenger_first_name='John',
            passenger_last_name='Doe',
            extra_luggage=0
        )

        self.checkin_url = reverse('passengers:checkin', args={self.ticket_no_checkin.id})
        self.delete_checkin_url = reverse('passengers:delete checkin', args={self.checkin.id})
        self.gate_register_url = reverse('passengers:gate register', args={self.ticket_checkin.id})
        return super().setUp()

    def test_checkin_GET(self):
        response = self.client.get(self.checkin_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/passengers/checkin/1/')

    def test_delete_checkin_GET(self):
        response = self.client.get(self.delete_checkin_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/passengers/checkin/delete/2/')

    def test_gate_register_GET(self):
        response = self.client.get(self.gate_register_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/passengers/gate/6/')
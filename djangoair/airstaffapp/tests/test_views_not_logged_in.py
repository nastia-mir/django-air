from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import MyUser, Staff, Passenger

from airuserapp.models import Ticket, CheckIn, BoardingPass

from airstaffapp.models import LunchOptions, LuggageOptions, Flight, FlightDate


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('staff:home')
        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/')


class TestStaffListViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_list_url = reverse('staff:staff list')
        self.edit_role_url = reverse('staff:edit role', args={1})

        self.user = MyUser.objects.create_user(
            email='teststaff@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.staff_account = Staff.objects.create(
            user=self.user,
            role='gate_manager'
        )
        return super().setUp()

    def test_staff_list_GET(self):
        response = self.client.get(self.staff_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/staff_list/')

    def test_edit_role_GET(self):
        response = self.client.get(self.edit_role_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/staff_list/1/')


class TestLunchLuggageViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.lunch_options_url = reverse('staff:lunch options')
        self.delete_lunch_url = reverse('staff:delete lunch', args={1})
        self.luggage_options_url = reverse('staff:luggage options')
        self.delete_luggage_url = reverse('staff:delete luggage', args={1})

        self.lunch = LunchOptions.objects.create(
            description='Soup',
            price=20
        )
        self.luggage = LuggageOptions.objects.create(
            quantity='0',
            price=20
        )
        return super().setUp()

    def test_lunch_options_GET(self):
        response = self.client.get(self.lunch_options_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/lunch/')

    def test_delete_lunch_GET(self):
        response = self.client.get(self.delete_lunch_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/lunch/1/delete/')

    def test_luggage_options_GET(self):
        response = self.client.get(self.luggage_options_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/luggage/')

    def test_delete_luggage_GET(self):
        response = self.client.get(self.delete_luggage_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/luggage/1/delete/')


class TestFlightsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.flights_url = reverse('staff:flights')
        self.create_flight_url = reverse('staff:create flight')
        self.flight_details_url = reverse('staff:flight details', args={1})
        self.cancel_flight_url = reverse('staff:cancel flight', args={1})
        self.canceled_flights_url = reverse('staff:canceled flights')

        self.date = FlightDate.objects.create(date='2023-03-23')
        self.flight = Flight.objects.create(
            destination='lisbon',
            date=self.date,
            passengers=60,
            ticket_price=30,
            extra_luggage_price=30
        )
        return super().setUp()

    def test_flights_GET(self):
        response = self.client.get(self.flights_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/flights/')

    def test_create_flights_GET(self):
        response = self.client.get(self.create_flight_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/flights/create/')

    def test_flights_details_GET(self):
        response = self.client.get(self.flight_details_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/flights/1/details/')

    def test_cancel_flight_GET(self):
        response = self.client.get(self.cancel_flight_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/flights/1/cancel/')

    def test_cancelled_flights_GET(self):
        response = self.client.get(self.canceled_flights_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/flights/canceled/')


class TestCheckinGateViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.checkin_list_url = reverse('staff:checkin list')
        self.checkin_url = reverse('staff:checkin', args={1})
        self.gate_list_url = reverse('staff:gate list')
        self.gate_register_url = reverse('staff:gate register', args={1})

        self.user = MyUser.objects.create_user(
            email='teststaff@gmail.com',
            password='strongpassword',
        )
        self.passenger = Passenger.objects.create(user=self.user)

        self.date = FlightDate.objects.create(date='2023-03-23')
        self.flight = Flight.objects.create(
            destination='lisbon',
            date=self.date,
            passengers=60,
            ticket_price=30,
            extra_luggage_price=30
        )

        self.ticket = Ticket.objects.create(
            passenger=self.passenger,
            flight=self.flight,
            tickets_quantity=1,
        )
        self.checkin = CheckIn.objects.create(
            ticket=self.ticket,
            passenger_first_name='John',
            passenger_last_name='Doe',
            extra_luggage=1
        )
        self.boarding_pass = BoardingPass.objects.create(
            ticket=self.ticket,
            passenger_first_name='John',
            passenger_last_name='Doe',
            extra_luggage=1,
            code='QWERTYUIOP'
        )
        return super().setUp()

    def test_checkin_list_GET(self):
        response = self.client.get(self.checkin_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/checkin/')

    def test_checkin_GET(self):
        response = self.client.get(self.checkin_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/checkin/1/')

    def test_gate_list_GET(self):
        response = self.client.get(self.gate_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/gate/')

    def test_gate_register_GET(self):
        response = self.client.get(self.gate_register_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/staff/gate/1/')
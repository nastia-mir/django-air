from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from accounts.models import MyUser, Staff, Passenger

from airuserapp.models import Ticket, CheckIn, BoardingPass

from airstaffapp.models import Flight, FlightDate


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('staff:home')
        self.login_url = reverse('accounts:login')

        self.user = MyUser.objects.create_user(
            email='test@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.staff_account = Staff.objects.create(
            user=self.user,
            role='gate_manager'
        )
        self.login_data = {'email': 'test@gmail.com',
                           'password': 'strongpassword'}
        self.client.post(self.login_url, self.login_data)
        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_staff.html')


class TestStaffListViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_list_url = reverse('staff:staff list')
        self.login_url = reverse('accounts:login')

        self.gate_manager_user = MyUser.objects.create_user(
            email='testgatemanager@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.gate_manager_staff_account = Staff.objects.create(
            user=self.gate_manager_user,
            role='gate_manager'
        )
        self.edit_role_url = reverse('staff:edit role', args={self.gate_manager_staff_account.id})

        self.login_data_gate_manager = {
            'email': 'testgatemanager@gmail.com',
            'password': 'strongpassword'
        }

        self.supervisor_user = MyUser.objects.create_user(
            email='testsupervisor@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.supervisor_staff_account = Staff.objects.create(
            user=self.supervisor_user,
            role='supervisor'
        )
        self.login_data_supervisor = {
            'email': 'testsupervisor@gmail.com',
            'password': 'strongpassword'
        }

        self.edit_role_data = {'role': 'checkin_manager'}
        return super().setUp()

    def test_staff_list_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.staff_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_list.html')

    def test_staff_list_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.staff_list_url)
        self.assertEqual(response.status_code, 403)

    def test_edit_role_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.edit_role_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_role.html')

    def test_edit_role_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.edit_role_url)
        self.assertEqual(response.status_code, 403)

    def test_edit_role_POST_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.edit_role_url, self.edit_role_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.staff_list_url)

    def test_edit_role_POST_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.post(self.edit_role_url, self.edit_role_data)
        self.assertEqual(response.status_code, 403)


class TestLunchLuggageViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.lunch_options_url = reverse('staff:lunch options')
        self.delete_lunch_url = reverse('staff:delete lunch', args={1})
        self.luggage_options_url = reverse('staff:luggage options')
        self.delete_luggage_url = reverse('staff:delete luggage', args={1})

        self.gate_manager_user = MyUser.objects.create_user(
            email='testgatemanager@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.gate_manager_staff_account = Staff.objects.create(
            user=self.gate_manager_user,
            role='gate_manager'
        )
        self.login_data_gate_manager = {
            'email': 'testgatemanager@gmail.com',
            'password': 'strongpassword'
        }

        self.supervisor_user = MyUser.objects.create_user(
            email='testsupervisor@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.supervisor_staff_account = Staff.objects.create(
            user=self.supervisor_user,
            role='supervisor'
        )
        self.login_data_supervisor = {
            'email': 'testsupervisor@gmail.com',
            'password': 'strongpassword'
        }
        self.lunch_data_valid = {
            'description': 'Soup',
            'price': 20
        }
        self.luggage_data_valid = {
            'quantity': '0',
            'price': 20
        }
        return super().setUp()

    def test_lunch_options_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.lunch_options_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lunch_options.html')

    def test_lunch_options_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.lunch_options_url)
        self.assertEqual(response.status_code, 403)

    def test_lunch_options_POST_supervisor_valid_data(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.lunch_options_url, self.lunch_data_valid)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.lunch_options_url)

    def test_lunch_options_POST_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.post(self.lunch_options_url, self.lunch_data_valid)
        self.assertEqual(response.status_code, 403)

    def test_delete_lunch_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        self.client.post(self.lunch_options_url, self.lunch_data_valid)
        response = self.client.get(self.delete_lunch_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.lunch_options_url)

    def test_delete_lunch_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.delete_lunch_url)
        self.assertEqual(response.status_code, 403)

    def test_luggage_options_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.luggage_options_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'luggage_options.html')

    def test_luggage_options_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.luggage_options_url)
        self.assertEqual(response.status_code, 403)

    def test_luggage_options_POST_supervisor_valid_data(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.luggage_options_url, self.luggage_data_valid)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.luggage_options_url)

    def test_luggage_options_POST_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.post(self.luggage_options_url, self.luggage_data_valid)
        self.assertEqual(response.status_code, 403)

    def test_delete_luggage_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        self.client.post(self.luggage_options_url, self.luggage_data_valid)
        response = self.client.get(self.delete_luggage_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.luggage_options_url)

    def test_delete_luggage_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.delete_luggage_url)
        self.assertEqual(response.status_code, 403)


class TestFlightsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.flights_url = reverse('staff:flights')
        self.create_flight_url = reverse('staff:create flight')
        self.canceled_flights_url = reverse('staff:canceled flights')

        self.gate_manager_user = MyUser.objects.create_user(
            email='testgatemanager@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.gate_manager_staff_account = Staff.objects.create(
            user=self.gate_manager_user,
            role='gate_manager'
        )
        self.login_data_gate_manager = {
            'email': 'testgatemanager@gmail.com',
            'password': 'strongpassword'
        }

        self.supervisor_user = MyUser.objects.create_user(
            email='testsupervisor@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.supervisor_staff_account = Staff.objects.create(
            user=self.supervisor_user,
            role='supervisor'
        )
        self.login_data_supervisor = {
            'email': 'testsupervisor@gmail.com',
            'password': 'strongpassword'
        }

        self.date = FlightDate.objects.create(date='2023-03-23')
        self.flight = Flight.objects.create(
            destination='lisbon',
            date=self.date,
            passengers=60,
            ticket_price=30,
            extra_luggage_price=30
        )
        self.flight_details_url = reverse('staff:flight details', args={self.flight.id})
        self.cancel_flight_url = reverse('staff:cancel flight', args={self.flight.id})

        self.create_flight_valid = {
            'date': '2023-03-17',
            'destination': 'Nairobi',
            'passengers': 60,
            'ticket_price': 30,
            'lunch': [],
            'luggage': [],
            'extra_luggage_price': 20
        }
        self.create_flight_invalid_prices = {
            'date': '2023-03-17',
            'destination': 'Nairobi',
            'passengers': '60',
            'ticket_price': '30',
            'lunch': [],
            'luggage': [],
            'extra_luggage_price': '20'
        }
        self.create_flight_invalid_destination = {
            'date': '2023-03-17',
            'destination': 'somecity',
            'passengers': '60',
            'ticket_price': '30',
            'lunch': [],
            'luggage': [],
            'extra_luggage_price': '20'
        }
        return super().setUp()

    def test_flights_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.flights_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flights.html')

    def test_flights_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.flights_url)
        self.assertEqual(response.status_code, 403)

    def test_create_flight_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.create_flight_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_flight.html')

    def test_create_flight_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.create_flight_url)
        self.assertEqual(response.status_code, 403)

    def test_create_flight_POST_supervisor_valid_data(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.create_flight_url, self.create_flight_valid)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.flights_url)

    def test_create_flight_POST_supervisor_invalid_prices(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.create_flight_url, self.create_flight_invalid_prices)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.create_flight_url)
        messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("Something went wrong. Please check if provided data is valid." in messages[0].message)

    def test_create_flight_POST_supervisor_invalid_destination(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.create_flight_url, self.create_flight_invalid_destination)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.create_flight_url)
        messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(messages[0].tags, "error")
        self.assertTrue("Something went wrong. Please check if provided data is valid." in messages[0].message)

    def test_create_flight_POST_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.post(self.create_flight_url, self.create_flight_valid)
        self.assertEqual(response.status_code, 403)

    def test_flights_details_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.flight_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_details.html')

    def test_flights_details_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.flight_details_url)
        self.assertEqual(response.status_code, 403)

    def test_cancel_flight_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.cancel_flight_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancel_flight.html')

    def test_cancel_flight_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.cancel_flight_url)
        self.assertEqual(response.status_code, 403)

    def test_cancel_flight_POST_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.cancel_flight_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.flights_url)

    def test_cancel_flight_POST_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.post(self.cancel_flight_url)
        self.assertEqual(response.status_code, 403)

    def test_cancelled_flights_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.canceled_flights_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'canceled_flights_list.html')

    def test_cancelled_flights_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.canceled_flights_url)
        self.assertEqual(response.status_code, 403)


class TestCheckinGateViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.checkin_list_url = reverse('staff:checkin list')
        self.gate_list_url = reverse('staff:gate list')

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
        self.checkin_url = reverse('staff:checkin', args={self.checkin.id})
        self.gate_register_url = reverse('staff:gate register', args={self.boarding_pass.id})

        self.gate_manager_user = MyUser.objects.create_user(
            email='testgatemanager@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.gate_manager_staff_account = Staff.objects.create(
            user=self.gate_manager_user,
            role='gate_manager'
        )
        self.login_data_gate_manager = {
            'email': 'testgatemanager@gmail.com',
            'password': 'strongpassword'
        }

        self.checkin_manager_user = MyUser.objects.create_user(
            email='testcheckinmanager@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.checkin_manager_staff_account = Staff.objects.create(
            user=self.checkin_manager_user,
            role='checkin_manager'
        )
        self.login_data_checkin_manager = {
            'email': 'testcheckinmanager@gmail.com',
            'password': 'strongpassword'
        }

        self.supervisor_user = MyUser.objects.create_user(
            email='testsupervisor@gmail.com',
            password='strongpassword',
            is_airlines_staff=True
        )
        self.supervisor_staff_account = Staff.objects.create(
            user=self.supervisor_user,
            role='supervisor'
        )
        self.login_data_supervisor = {
            'email': 'testsupervisor@gmail.com',
            'password': 'strongpassword'
        }

        return super().setUp()

    def test_checkin_list_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.checkin_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_list.html')

    def test_checkin_list_GET_checkin_manager_has_access(self):
        self.client.post(self.login_url, self.login_data_checkin_manager)
        response = self.client.get(self.checkin_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_list.html')

    def test_checkin_list_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.checkin_list_url)
        self.assertEqual(response.status_code, 403)

    def test_checkin_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.checkin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin.html')

    def test_checkin_GET_checkin_manager_has_access(self):
        self.client.post(self.login_url, self.login_data_checkin_manager)
        response = self.client.get(self.checkin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin.html')

    def test_checkin_GET_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.checkin_url)
        self.assertEqual(response.status_code, 403)

    def test_checkin_POST_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.checkin_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.checkin_url)

    def test_checkin_POST_checkin_manager_has_access(self):
        self.client.post(self.login_url, self.login_data_checkin_manager)
        response = self.client.post(self.checkin_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.checkin_url)

    def test_checkin_POST_gate_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.post(self.checkin_url)
        self.assertEqual(response.status_code, 403)

    def test_gate_list_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.gate_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate_list.html')

    def test_gate_list_GET_gate_manager_has_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.gate_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate_list.html')

    def test_gate_list_GET_checkin_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_checkin_manager)
        response = self.client.get(self.gate_list_url)
        self.assertEqual(response.status_code, 403)

    def test_gate_register_GET_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.get(self.gate_register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate_approve.html')

    def test_gate_register_GET_gate_manager_has_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.get(self.gate_register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate_approve.html')

    def test_gate_register_GET_checkin_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_checkin_manager)
        response = self.client.get(self.gate_register_url)
        self.assertEqual(response.status_code, 403)

    def test_gate_register_POST_supervisor_has_access(self):
        self.client.post(self.login_url, self.login_data_supervisor)
        response = self.client.post(self.gate_register_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.gate_register_url)

    def test_gate_register_POST_gate_manager_has_access(self):
        self.client.post(self.login_url, self.login_data_gate_manager)
        response = self.client.post(self.gate_register_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.gate_register_url)

    def test_gate_register_POST_checkin_manager_no_access(self):
        self.client.post(self.login_url, self.login_data_checkin_manager)
        response = self.client.post(self.gate_register_url)
        self.assertEqual(response.status_code, 403)

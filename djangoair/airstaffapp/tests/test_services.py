from django.test import TestCase

from airuserapp.models import Ticket, CheckIn, BoardingPass

from accounts.models import MyUser, Passenger

from airstaffapp.models import LunchOptions, LuggageOptions, Flight, FlightDate
from airstaffapp.services import CreateBoardingPass


class TestServices(TestCase):
    def setUp(self):
        self.lunch = LunchOptions.objects.create(description='Soup', price=10)
        self.luggage = LuggageOptions.objects.create(quantity='1', price=20)
        self.date = FlightDate.objects.create(date='2023-05-12')
        self.flight = Flight.objects.create(
            destination='lisbon',
            date=self.date,
            passengers=40,
            ticket_price=40,
            extra_luggage_price=40
        )
        self.user = MyUser.objects.create_user('test@gmail.com', 'strongpassword')
        self.passenger = Passenger.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            passenger=self.passenger,
            flight=self.flight,
            tickets_quantity=2,
            lunch=self.lunch,
            luggage=self.luggage
        )
        self.checkin_completed = CheckIn.objects.create(
            ticket=self.ticket,
            passenger_first_name='Jane',
            passenger_last_name='Doe',
            extra_luggage=0,
            status='completed'
        )

        self.checkin_in_progress = CheckIn.objects.create(
            ticket=self.ticket,
            passenger_first_name='Jane',
            passenger_last_name='Doe',
            extra_luggage=0,
            status='in_progress'
        )

        return super().setUp()

    def test_create_boarding_pass_checkin_completed(self):
        CreateBoardingPass.create_boarding_pass(self.checkin_completed)
        boarding_pass = list(BoardingPass.objects.filter(ticket=self.ticket))
        self.assertTrue(boarding_pass)
        self.assertEqual(len(boarding_pass), 1)

    def test_create_boarding_pass_checkin_in_progress(self):
        CreateBoardingPass.create_boarding_pass(self.checkin_in_progress)
        boarding_pass = list(BoardingPass.objects.filter(ticket=self.ticket))
        self.assertFalse(boarding_pass)
        self.assertEqual(len(boarding_pass), 0)

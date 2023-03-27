from django.test import SimpleTestCase
from django.urls import reverse, resolve

from airstaffapp import views


class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse('staff:home')
        self.assertEqual(resolve(url).func.__name__, views.HomeView.as_view().__name__)

    def test_staff_list(self):
        url = reverse('staff:staff list')
        self.assertEqual(resolve(url).func.__name__, views.StaffListView.as_view().__name__)

    def test_edit_role(self):
        url = reverse('staff:edit role', args=['1'])
        self.assertEqual(resolve(url).func.__name__, views.EditRoleView.as_view().__name__)

    def test_lunch_options(self):
        url = reverse('staff:lunch options')
        self.assertEqual(resolve(url).func.__name__, views.LunchOptionsView.as_view().__name__)

    def test_delete_lunch(self):
        url = reverse('staff:delete lunch', args=['1'])
        self.assertEqual(resolve(url).func.__name__, views.LunchOptionsDeleteView.as_view().__name__)

    def test_luggage_options(self):
        url = reverse('staff:luggage options')
        self.assertEqual(resolve(url).func.__name__, views.LuggageOptionsView.as_view().__name__)

    def test_delete_luggage(self):
        url = reverse('staff:delete luggage', args=['1'])
        self.assertEqual(resolve(url).func.__name__, views.LuggageOptionsDeleteView.as_view().__name__)

    def test_flights(self):
        url = reverse('staff:flights')
        self.assertEqual(resolve(url).func.__name__, views.FlightsView.as_view().__name__)

    def test_create_flight(self):
        url = reverse('staff:create flight')
        self.assertEqual(resolve(url).func.__name__, views.CreateFlightView.as_view().__name__)

    def test_flight_details(self):
        url = reverse('staff:flight details', args=['1'])
        self.assertEqual(resolve(url).func.__name__, views.FlightDetailsView.as_view().__name__)

    def test_cancel_flight(self):
        url = reverse('staff:cancel flight', args=['1'])
        self.assertEqual(resolve(url).func.__name__, views.CancelFlightView.as_view().__name__)

    def test_canceled_flights(self):
        url = reverse('staff:canceled flights')
        self.assertEqual(resolve(url).func.__name__, views.CanceledFLightsListView.as_view().__name__)

    def test_checkin_list(self):
        url = reverse('staff:checkin list')
        self.assertEqual(resolve(url).func.__name__, views.CheckInListView.as_view().__name__)

    def test_checkin(self):
        url = reverse('staff:checkin', args=['1'])
        self.assertEqual(resolve(url).func.__name__, views.CheckInView.as_view().__name__)

    def test_gate_list(self):
        url = reverse('staff:gate list')
        self.assertEqual(resolve(url).func.__name__, views.GateListView.as_view().__name__)

    def test_gate_register(self):
        url = reverse('staff:gate register', args=['1'])
        self.assertEqual(resolve(url).func.__name__, views.GateView.as_view().__name__)
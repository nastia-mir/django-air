from django.test import SimpleTestCase
from django.urls import reverse, resolve

from airuserapp import views


class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse('passengers:home')
        self.assertEqual(resolve(url).func.__name__, views.HomeView.as_view().__name__)

    def test_tickets(self):
        url = reverse('passengers:tickets')
        self.assertEqual(resolve(url).func.__name__, views.SearchTicketsView.as_view().__name__)

    def test_ticket_details(self):
        url = reverse('passengers:ticket details', args={1})
        self.assertEqual(resolve(url).func.__name__, views.TicketDetailsView.as_view().__name__)

    def test_ticket_booking(self):
        url = reverse('passengers:ticket booking', args={1})
        self.assertEqual(resolve(url).func.__name__, views.TicketBookingView.as_view().__name__)

    def test_load_dates_ajax(self):
        url = reverse('passengers:ajax load dates')
        self.assertEqual(resolve(url).func, views.load_dates)

    def test_view_ticket(self):
        url = reverse('passengers:view ticket', args={1})
        self.assertEqual(resolve(url).func.__name__, views.ViewTicketView.as_view().__name__)

    def test_checkin(self):
        url = reverse('passengers:checkin', args={1})
        self.assertEqual(resolve(url).func.__name__, views.CheckInView.as_view().__name__)

    def test_delete_checkin(self):
        url = reverse('passengers:delete checkin', args={1})
        self.assertEqual(resolve(url).func.__name__, views.DeleteFromCheckin.as_view().__name__)

    def test_gate_register(self):
        url = reverse('passengers:gate register', args={1})
        self.assertEqual(resolve(url).func.__name__, views.GateRegisterView.as_view().__name__)

    def test_ticket_payment(self):
        url = reverse('passengers:ticket payment', args={1, 10})
        self.assertEqual(resolve(url).func.__name__, views.ProcessTicketPaymentView.as_view().__name__)

    def test_extra_luggage_payment(self):
        url = reverse('passengers:extra luggage payment', args={1, 10})
        self.assertEqual(resolve(url).func.__name__, views.ProcessExtraLuggagePaymentView.as_view().__name__)

    def test_refund(self):
        url = reverse('passengers:refund', args={1})
        self.assertEqual(resolve(url).func.__name__, views.RefundView.as_view().__name__)

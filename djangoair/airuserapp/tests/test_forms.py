from django.test import TestCase

from airuserapp import forms

from airstaffapp.models import Flight, FlightDate, LunchOptions, LuggageOptions


class TestForms(TestCase):
    def test_CheckInForm_valid_data(self):
        form = forms.CheckInForm(data={
            'passenger_first_name': 'John',
            'passenger_last_name': 'Doe',
            'extra_luggage': 1
        })
        self.assertTrue(form.is_valid())

    def test_CheckInForm_invalid_data(self):
        form = forms.CheckInForm(data={
            'passenger_first_name': 'John',
            'passenger_last_name': 'Doe',
            'extra_luggage': 'luggage'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_CheckInForm_no_data(self):
        form = forms.CheckInForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
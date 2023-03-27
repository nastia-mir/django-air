from django.test import TestCase

from airstaffapp import forms
from airstaffapp.models import LuggageOptions, LunchOptions


class TestForms(TestCase):
    def setUp(self):
        self.lunch = LunchOptions.objects.create(description='Soup', price=10)
        self.luggage = LuggageOptions.objects.create(quantity='1', price=20)
        return super().setUp()

    def test_StaffRoleEditForm_valid_data(self):
        form = forms.StaffRoleEditForm(data={
            'role': 'supervisor',
        })
        self.assertTrue(form.is_valid())

    def test_StaffRoleEditForm_invalid_data(self):
        form = forms.StaffRoleEditForm(data={
            'role': 'somerole',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_StaffRoleEditForm_no_data_valid_form(self):
        form = forms.StaffRoleEditForm(data={})
        self.assertTrue(form.is_valid())

    def test_LunchOptionsForm_valid_data(self):
        form = forms.LunchOptionsForm(data={
            'description': 'Lasagna',
            'price': 20
        })
        self.assertTrue(form.is_valid())

    def test_LunchOptionsForm_no_data_invalid_form(self):
        form = forms.LunchOptionsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_LuggageOptionsForm_valid_data(self):
        form = forms.LuggageOptionsForm(data={
            'quantity': 1,
            'price': 20
        })
        self.assertTrue(form.is_valid())

    def test_LuggageOptionsForm_invalid_data(self):
        form = forms.LuggageOptionsForm(data={
            'quantity': '4',
            'price': 20
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_LuggageOptionsForm_no_data_invalid_form(self):
        form = forms.LuggageOptionsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_DateForm_valid_data(self):
        form = forms.DateForm(data={
            'date': '2023-05-23'
        })
        self.assertTrue(form.is_valid())

    def test_DateForm_invalid_data(self):
        form = forms.DateForm(data={
            'date': '23445'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_DateForm_no_data_invalid_form(self):
        form = forms.DateForm(data={
            'date': '23445'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_FlightCreationForm_valid_data(self):
        form = forms.FlightCreationForm(data={
            'destination': 'lisbon',
            'passengers': 30,
            'ticket_price': 30,
            'lunch': [self.lunch],
            'luggage': [self.luggage],
            'extra_luggage_price': 40
        })
        self.assertTrue(form.is_valid())

    def test_FlightCreationForm_invalid_data(self):
        form = forms.FlightCreationForm(data={
            'destination': 'kyiv',
            'passengers': 30,
            'ticket_price': 30,
            'lunch': 'lunch',
            'luggage': 'luggage',
            'extra_luggage_price': 40
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_FlightCreationForm_no_data_invalid_form(self):
        form = forms.FlightCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)


from django.test import TestCase

from accounts import forms


class TestForms(TestCase):
    def test_MyUserCreationForm_valid_data(self):
        form = forms.MyUserCreationForm(data={
            'email': 'test@gmail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'strongpassword',
            'password2': 'strongpassword',
            'is_airlines_staff': True
        })
        self.assertTrue(form.is_valid())

    def test_MyUserCreationForm_no_data_form_invalid(self):
        form = forms.MyUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_EmailForm_valid_data(self):
        form = forms.EmailForm(data={
            'email': 'test@gmail.com',
        })
        self.assertTrue(form.is_valid())

    def test_EmailForm_no_data_form_invalid(self):
        form = forms.EmailForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_EmailForm_invalid_data(self):
        form = forms.EmailForm(data={
            'email': 'test',
        })
        self.assertFalse(form.is_valid())

    def test_EditProfileForm_valid_data(self):
        form = forms.EditProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertTrue(form.is_valid())

    def test_EditProfileForm_no_data_form_valid(self):
        form = forms.EditProfileForm(data={})
        self.assertTrue(form.is_valid())


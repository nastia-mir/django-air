from django.test import TestCase

from accounts.services import PasswordGenerator


class TestServices(TestCase):
    def test_generated_password_is_string(self):
        password = PasswordGenerator.generate_password()
        self.assertTrue(isinstance(password, str))

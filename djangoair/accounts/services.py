from django.utils.crypto import get_random_string


class PasswordGenerator:
    @classmethod
    def generate_password(self):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        password = get_random_string(15, chars)
        return password


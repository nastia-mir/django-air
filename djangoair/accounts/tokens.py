from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivatorTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.id) + six.text_type(timestamp) + six.text_type(user.is_airlines_staff)


account_activation_token = AccountActivatorTokenGenerator()

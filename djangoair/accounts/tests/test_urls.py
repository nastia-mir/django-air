from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts import views


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.__name__, views.LoginView.as_view().__name__)

    def test_register(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.__name__, views.RegisterView.as_view().__name__)

    def test_logout(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.__name__, views.LogoutView.as_view().__name__)

    def test_edit_profile(self):
        url = reverse('accounts:edit profile')
        self.assertEqual(resolve(url).func.__name__, views.EditProfileView.as_view().__name__)

    def test_change_password(self):
        url = reverse('accounts:change password')
        self.assertEqual(resolve(url).func.__name__, views.ChangePasswordView.as_view().__name__)

    def test_restore_password(self):
        url = reverse('accounts:restore password')
        self.assertEqual(resolve(url).func.__name__, views.RestorePasswordView.as_view().__name__)

    def test_reset_password(self):
        url = reverse('accounts:reset password', args={'ddd', 'dferf'})
        self.assertEqual(resolve(url).func.__name__, views.ResetPasswordView.as_view().__name__)
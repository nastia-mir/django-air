from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import MyUser


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.register_url = reverse('accounts:register')
        self.edit_profile_url = reverse('accounts:edit profile')
        self.change_password_url = reverse('accounts:change password')
        self.restore_password_url = reverse('accounts:restore password')

        self.user = MyUser.objects.create_user(
            email='test@gmail.com',
            password='strongpassword'
        )

        self.login_data_valid = {
            'email': 'test@gmail.com',
            'password': 'strongpassword'
        }

        self.login_data_incorrect_password = {
            'email': 'test@gmail.com',
            'password': 'notsostrongpassword'
        }

        self.login_data_user_dont_exist = {
            'email': 'testnotexist@gmail.com',
            'password': 'strongpassword'
        }

        self.register_data_valid = {
            'email': 'testregister@gmail.com',
            'password1': 'strongpassword',
            'password2': 'strongpassword'
        }

        self.register_data_password_not_match = {
            'email': 'testregister@gmail.com',
            'password1': 'strongpassword',
            'password2': 'strongpassword1'
        }

        self.register_data_user_exists = {
            'email': 'test@gmail.com',
            'password1': 'strongpassword',
            'password2': 'strongpassword'
        }

        self.edit_profile_data_valid = {
            'first_name': 'Jane',
            'last_name': 'Doe'
        }

        self.change_password_valid_data = {
            'old_password': 'strongpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        }

        self.change_password_incorrect_old_password = {
            'old_password': 'notsostrongpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        }

        self.restore_password_valid_email = {'email': 'test@gmail.com'}
        self.restore_password_user_not_exists = {'email': 'testnotexists@gmail.com'}

        return super().setUp()

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_POST_valid(self):
        response = self.client.post(self.login_url, self.login_data_valid)
        self.assertEqual(response.status_code, 302)

    def test_login_POST_incorrect_password(self):
        response = self.client.post(self.login_url, self.login_data_incorrect_password)
        self.assertEqual(response.status_code, 302)

    def test_login_POST_user_dont_exist(self):
        response = self.client.post(self.login_url, self.login_data_user_dont_exist)
        self.assertEqual(response.status_code, 302)

    def test_logout_GET_logged_in(self):
        self.client.post(self.login_url, self.login_data_valid)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_logout_GET_not_logged_in(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_POST_valid(self):
        response = self.client.post(self.register_url, self.register_data_valid)
        self.assertEqual(response.status_code, 302)

    def test_register_POST_password_not_match(self):
        response = self.client.post(self.register_url, self.register_data_password_not_match)
        self.assertEqual(response.status_code, 200)

    def test_register_POST_user_exist(self):
        response = self.client.post(self.register_url, self.register_data_user_exists)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_GET_logged_in(self):
        self.client.post(self.login_url, self.login_data_valid)
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_edit_profile_GET_not_logged_in(self):
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_POST_valid(self):
        self.client.post(self.login_url, self.login_data_valid)
        response = self.client.post(self.edit_profile_url, self.edit_profile_data_valid)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_POST_no_data(self):
        self.client.post(self.login_url, self.login_data_valid)
        response = self.client.post(self.edit_profile_url, {})
        self.assertEqual(response.status_code, 302)

    def test_change_password_GET_logged_in(self):
        self.client.post(self.login_url, self.login_data_valid)
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_change_password_GET_not_logged_in(self):
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 302)

    def test_change_password_POST_valid(self):
        self.client.post(self.login_url, self.login_data_valid)
        response = self.client.post(self.change_password_url, self.change_password_valid_data)
        self.assertEqual(response.status_code, 302)

    def test_change_password_POST_incorrect_old_password(self):
        self.client.post(self.login_url, self.login_data_valid)
        response = self.client.post(self.change_password_url, self.change_password_incorrect_old_password)
        self.assertEqual(response.status_code, 302)

    def test_restore_password_GET(self):
        response = self.client.get(self.restore_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restore_password.html')

    def test_restore_password_POST_data_valid(self):
        response = self.client.post(self.restore_password_url, self.restore_password_valid_email)
        self.assertEqual(response.status_code, 302)

    def test_restore_password_POST_user_not_exists(self):
        response = self.client.post(self.restore_password_url, self.restore_password_user_not_exists)
        self.assertEqual(response.status_code, 302)
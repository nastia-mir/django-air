from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField
from accounts.models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'is_airlines_staff']


class PassengerForm(Form):
    email = EmailField(max_length = 200)



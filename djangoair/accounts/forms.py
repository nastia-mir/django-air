from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from accounts.models import MyUser


class StaffCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password1', 'password2', 'is_airlines_staff']


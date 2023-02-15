from django.contrib.auth.forms import UserCreationForm
from accounts.models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password1', 'password2', 'is_airlines_staff']


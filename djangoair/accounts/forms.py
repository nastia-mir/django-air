from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField, ModelForm
from accounts.models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'is_airlines_staff']


class EmailForm(Form):
    email = EmailField(max_length=200)


class EditProfileForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name']



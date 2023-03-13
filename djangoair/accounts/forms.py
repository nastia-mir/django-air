from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField, ModelForm, TextInput
from accounts.models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'is_airlines_staff']

        widgets = {
            'email': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'password1': TextInput(attrs={'class': 'form-control'}),
            'password2': TextInput(attrs={'class': 'form-control'}),
        }


class EmailForm(Form):
    email = EmailField(max_length=200, widget=TextInput(attrs={'class': 'form-control'}))


class EditProfileForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
        }



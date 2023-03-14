from django.views.generic import FormView
from django.views.generic.edit import ProcessFormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.forms import MyUserCreationForm, EditProfileForm, EmailForm
from accounts.models import MyUser, Staff, Passenger
from accounts.services import PasswordGenerator

from airuserapp.services import Emails


class LoginView(ProcessFormView):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            existing_user = MyUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('passengers:home')
        else:
            messages.error(request, 'Wrong email or password.')
            return redirect('accounts:login')

    def get(self, request):
        return render(request, "login.html")


class RegisterView(FormView):
    template_name = "register.html"
    form_class = MyUserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        try:
            existing_user = MyUser.objects.get(email=form.email)
            messages.error(self.request, 'This email is already used.')
            return redirect('accounts:register')
        except:
            user = form.save(commit=False)
            #user.email = user.email.lower()
            user.save()
            passenger_account = Passenger.objects.create(user=user)
            passenger_account.save()
        return super().form_valid(form)


class LogoutView(ProcessFormView):
    def get(self, request):
        logout(request)
        return redirect('passengers:home')


class EditProfileView(ProcessFormView):
    def get(self, request):
        context = {'form': EditProfileForm(instance=request.user)}
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            request.user.first_name = user_form.first_name
            request.user.last_name = user_form.last_name
            request.user.save()
            return redirect('passengers:home')
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('passengers:edit profile')


class ChangePasswordView(ProcessFormView):
    def get(self, request):
        context = {'form': PasswordChangeForm(request.user)}
        return render(request, 'change_password.html', context)

    def post(self, request):
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            login(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('passengers:home')
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('accounts:change password')


class RestorePasswordView(ProcessFormView):
    def get(self, request):
        context = {'form': EmailForm}
        return render(request, 'restore_password.html', context)

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = MyUser.objects.get(email=email)
                new_password = PasswordGenerator.generate_password()
                user.set_password(new_password)
                user.save()
                Emails.send_temporary_password(request, email, new_password)
                return redirect('accounts:login')
            except:
                messages.error(request, 'User with given email does not exist.')
                return redirect('accounts:restore password')

        else:
            messages.error(request, 'Please enter valid email.')
            return redirect('accounts:restore password')

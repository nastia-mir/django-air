from django.views.generic import FormView
from django.views.generic.edit import ProcessFormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from accounts.forms import MyUserCreationForm, EditProfileForm, EmailForm
from accounts.models import MyUser, Passenger
from accounts.tokens import account_activation_token

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
                Emails.send_password_resetting_link(request, user)
                return redirect('accounts:login')
            except:
                messages.error(request, 'User with given email does not exist.')
                return redirect('accounts:restore password')

        else:
            messages.error(request, 'Please enter valid email.')
            return redirect('accounts:restore password')


class ResetPasswordView(ProcessFormView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(id=uid)
        except:
            user = None

        if user and account_activation_token.check_token(user, token):
            context = {'form': SetPasswordForm(user)}
            return render(request, 'reset_password.html', context)
        else:
            messages.error('Something went wrong with password resetting link.')
            return redirect('account:login')

    def post(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(id=uid)
        password_form = SetPasswordForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            login(request, user)
            messages.success(request, 'Your password was successfully reset!')
            return redirect('passengers:home')
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('accounts:reset password', args={uidb64, token})


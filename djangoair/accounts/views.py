from django.views.generic import TemplateView, FormView, UpdateView
from django.views.generic.edit import ProcessFormView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, reverse

from accounts.forms import MyUserCreationForm, EditProfileForm
from accounts.models import MyUser, Staff, Passenger


class HomeView(TemplateView):
    template_name = "home.html"


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
            user.email = user.email.lower()
            user.save()
            if user.is_airlines_staff:
                staff_account = Staff.objects.create(user=user)
                staff_account.save()
            else:
                passenger_account = Passenger.objects.create(user=user)
                passenger_account.save()
            return super().form_valid(form)


class LogoutView(ProcessFormView):
    def get(self, request):
        logout(request)
        return redirect('passengers:home')


class EditProfileView(ProcessFormView):
    def get(self, request):
        context = {'form': EditProfileForm}
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            request.user.first_name = user_form.first_name
            request.user.last_name = user_form.last_name
            request.user.save()
            return redirect('passengers:home')


class ChangePasswordView(UpdateView):
    pass


class RestorePasswordView(UpdateView):
    pass
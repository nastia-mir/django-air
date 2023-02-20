from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.views import View
from django.shortcuts import render, redirect, reverse

from accounts.models import Staff

from airstaffapp.models import Flight, LunchOptions, LuggageOptions
from airstaffapp.forms import StaffRoleEditForm, FlightCreationForm, LunchOptionsForm, LuggageOptionsForm


class HomeView(TemplateView):
    template_name = "home_staff.html"

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()
        context['role'] = Staff.objects.get(user=self.request.user).role
        return context


class StaffListView(TemplateView):
    template_name = "staff_list.html"

    def get_context_data(self):
        context = super(StaffListView, self).get_context_data()
        staff = Staff.objects.all()
        editable_staff = []
        for person in staff:
            if person.role != 'supervisor':
                editable_staff.append(person)
        context['staff'] = editable_staff
        context['request_user_role'] = Staff.objects.get(user=self.request.user).role
        return context


class EditRoleView(UpdateView):
    template_name = "edit_role.html"
    form_class = StaffRoleEditForm
    model = Staff

    def get_success_url(self):
        return reverse('staff:staff list')

    def get_context_data(self):
        context = super(EditRoleView, self).get_context_data()
        person = Staff.objects.get(id=self.kwargs['pk'])
        context['person'] = person
        context['request_user_role'] = Staff.objects.get(user=self.request.user).role
        return context

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.save()
        return super().form_valid(form)


class FlightsView(TemplateView):
    template_name = 'flights.html'

    def get_context_data(self):
        context = super(FlightsView, self).get_context_data()
        flights = Flight.objects.all().order_by('date')
        context['request_user_role'] = Staff.objects.get(user=self.request.user).role
        if len(flights) == 0:
            context['empty'] = True
        else:
            context['flights'] = flights
        return context


class LunchOptionsView(CreateView):

    def get(self, request):
        context = {
            'options': LunchOptions.objects.all(),
            'request_user_role': Staff.objects.get(user=request.user).role,
            'form': LunchOptionsForm
        }
        return render(request, 'lunch_options.html', context)

    def post(self, request):
        form = LunchOptionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff:lunch options'))


class LunchOptionsDeleteView(DeleteView):

    def get(self, request, pk):
        lunch = LunchOptions.objects.get(id=pk)
        lunch.delete()
        return redirect(reverse('staff:lunch options'))


class LuggageOptionsView(CreateView):

    def get(self, request):
        context = {
            'options': LuggageOptions.objects.all(),
            'request_user_role': Staff.objects.get(user=request.user).role,
            'form': LuggageOptionsForm
        }
        return render(request, 'luggage_options.html', context)

    def post(self, request):
        form = LuggageOptionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff:luggage options'))


class LuggageOptionsDeleteView(DeleteView):

    def get(self, request, pk):
        luggage = LuggageOptions.objects.get(id=pk)
        luggage.delete()
        return redirect(reverse('staff:luggage options'))


class CreateFlightView(CreateView):

    def get(self, request):
        context = {
            'request_user_role': Staff.objects.get(user=request.user).role,
            'form': FlightCreationForm
        }
        return render(request, 'create_flight.html', context)

    def post(self, request):
        form = FlightCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff:flights'))


class CancelFlightView(UpdateView):
    template_name = 'cancel_flight.html'
    model = Flight
    fields = ['is_canceled']

    def get_context_data(self):
        context = super(CancelFlightView, self).get_context_data()
        flight = Flight.objects.get(id=self.kwargs['pk'])
        context['flight'] = flight
        context['request_user_role'] = Staff.objects.get(user=self.request.user).role
        return context

    def post(self, request, pk):
        try:
            flight = Flight.objects.get(id=self.kwargs['pk'])
            flight.is_canceled = True
            flight.save()
            return redirect(reverse('staff:flights'))
        except:
            return redirect(reverse('staff:flights'))









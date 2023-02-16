from django.views.generic import TemplateView, FormView, UpdateView, CreateView
from django.views.generic.edit import ProcessFormView, ModelFormMixin
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Staff
from airstaffapp.models import Flight, FlightOptions
from airstaffapp.forms import StaffRoleEditForm, FlightCreationForm, FlightOptionsForm


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
        if len(flights) == 0:
            context['empty'] = True
        else:
            context['flights'] = flights
        return context


class CreateFlightView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'flight_form': FlightCreationForm,
                   'options_form': FlightOptionsForm}
        return render(request, 'create_flight.html', context)

    def post(self, request, *args, **kwargs):
        flight_form = FlightCreationForm(request.POST)
        options_form = FlightOptionsForm(request.POST)
        if flight_form.is_valid() and options_form.is_valid():
            options = options_form.save()
            flight = flight_form.save(commit=False)
            flight.flight_options = options
            flight.save()
            return redirect(reverse('staff:flights'))
        return redirect(reverse('staff:flights'))


class EditFlightView(UpdateView):
    template_name = 'edit_flight.html'
    model = FlightOptions
    fields = '__all__'

    def get_success_url(self):
        return reverse('staff:flights')

    def get_context_data(self):
        context = super(EditFlightView, self).get_context_data()
        flight = Flight.objects.get(id=self.kwargs['pk'])
        context['flight'] = flight
        options = flight.flight_options
        context['options'] = options
        return context


class CancelFlightView(UpdateView):
    template_name = 'cancel_flight.html'
    model = Flight
    fields = ['is_canceled']

    def get_context_data(self):
        context = super(CancelFlightView, self).get_context_data()
        flight = Flight.objects.get(id=self.kwargs['pk'])
        context['flight'] = flight
        return context

    def post(self, request, pk):
        try:
            flight = Flight.objects.get(id=self.kwargs['pk'])
            flight.is_canceled = True
            flight.save()
            return redirect(reverse('staff:flights'))
        except:
            return redirect(reverse('staff:flights'))




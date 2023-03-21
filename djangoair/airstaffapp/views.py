from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, ListView
from django.views.generic.edit import ProcessFormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, reverse

from accounts.models import Staff, RoleOptions

from airstaffapp.models import Flight, FlightDate, LunchOptions, LuggageOptions
from airstaffapp.forms import StaffRoleEditForm, FlightCreationForm, LunchOptionsForm, LuggageOptionsForm, DateForm
from airstaffapp.services import CreateBoardingPass

from airuserapp.models import Ticket, CheckIn, BoardingPass, StatusOptions
from airuserapp.services import Emails


class HomeView(UserPassesTestMixin, TemplateView):
    template_name = "home_staff.html"

    def test_func(self):
        return self.request.user.is_airlines_staff

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()
        role = Staff.objects.get(user=self.request.user).role
        if role:
            context['role'] = True
        else:
            context['role'] = False
        if role == RoleOptions.supervisor.value:
            context['is_supervisor'] = True
            context['is_gate_manager'] = True
            context['is_checkin_manager'] = True
        elif role == RoleOptions.checkin_manager.value:
            context['is_supervisor'] = False
            context['is_gate_manager'] = False
            context['is_checkin_manager'] = True
        elif role == RoleOptions.gate_manager.value:
            context['is_supervisor'] = False
            context['is_gate_manager'] = True
        return context


class StaffListView(UserPassesTestMixin, TemplateView):
    template_name = "staff_list.html"

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get_context_data(self):
        context = super(StaffListView, self).get_context_data()
        staff = Staff.objects.all()
        editable_staff = []
        for person in staff:
            if person.role != RoleOptions.supervisor.value:
                editable_staff.append(person)
        context['staff'] = editable_staff
        request_user_role = Staff.objects.get(user=self.request.user).role
        if request_user_role == RoleOptions.supervisor.value:
            context['is_supervisor'] = True
        else:
            context['is_supervisor'] = False
        return context


class EditRoleView(UserPassesTestMixin, UpdateView):
    template_name = "edit_role.html"
    form_class = StaffRoleEditForm
    model = Staff

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get_success_url(self):
        return reverse('staff:staff list')

    def get_context_data(self):
        context = super(EditRoleView, self).get_context_data()
        person = Staff.objects.get(id=self.kwargs['pk'])
        context['person'] = person
        request_user_role = Staff.objects.get(user=self.request.user).role
        if request_user_role == RoleOptions.supervisor.value:
            context['is_supervisor'] = True
        else:
            context['is_supervisor'] = False
        return context

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.save()
        return super().form_valid(form)


class LunchOptionsView(UserPassesTestMixin, CreateView):
    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

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


class LunchOptionsDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get(self, request, pk):
        lunch = LunchOptions.objects.get(id=pk)
        lunch.delete()
        return redirect(reverse('staff:lunch options'))


class LuggageOptionsView(UserPassesTestMixin, CreateView):
    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get(self, request):
        context = {
            'options': LuggageOptions.objects.all(),
            'form': LuggageOptionsForm
        }
        return render(request, 'luggage_options.html', context)

    def post(self, request):
        form = LuggageOptionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('staff:luggage options'))


class LuggageOptionsDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get(self, request, pk):
        luggage = LuggageOptions.objects.get(id=pk)
        luggage.delete()
        return redirect(reverse('staff:luggage options'))


class FlightsView(UserPassesTestMixin, TemplateView):
    template_name = 'flights.html'

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get_context_data(self):
        context = super(FlightsView, self).get_context_data()
        flights = Flight.objects.all().order_by('date')
        if len(flights) == 0:
            context['empty'] = True
        else:
            context['flights'] = flights
        return context


class CreateFlightView(UserPassesTestMixin, CreateView):
    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get(self, request):
        context = {
            'flight_form': FlightCreationForm,
            'date_form': DateForm
        }
        return render(request, 'create_flight.html', context)

    def post(self, request):
        flight_form = FlightCreationForm(request.POST)
        date_form = DateForm(request.POST)
        if flight_form.is_valid() and date_form.is_valid():
            flight_date = date_form.save(commit=False)
            date, created = FlightDate.objects.get_or_create(date=flight_date.date)
            flight = flight_form.save(commit=False)
            flight.date = date
            flight.save()
            flight_form.save_m2m()
            return redirect(reverse('staff:flights'))
        else:
            messages.error(request, 'Something went wrong. Please check if provided data is valid.')
            return redirect(reverse('staff:create flight'))


class FlightDetailsView(UserPassesTestMixin, TemplateView):
    template_name = 'flight_details.html'

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get_context_data(self, pk):
        context = super(FlightDetailsView, self).get_context_data()
        flight = Flight.objects.get(id=pk)
        luggage = flight.luggage.all()
        lunch = flight.lunch.all()
        context['flight'] = flight
        context['luggage'] = list(luggage)
        context['lunch'] = list(lunch)
        return context


class CancelFlightView(UserPassesTestMixin, UpdateView):
    template_name = 'cancel_flight.html'
    model = Flight
    fields = ['is_canceled']

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get_context_data(self):
        context = super(CancelFlightView, self).get_context_data()
        context['flight'] = Flight.objects.get(id=self.kwargs['pk'])
        return context

    def post(self, request, pk):
        try:
            flight = Flight.objects.get(id=self.kwargs['pk'])
            flight.is_canceled = True
            flight.save()

            tickets = list(Ticket.objects.filter(flight=flight).all())
            for ticket in tickets:
                Emails.send_flight_cancellation_info(request, flight, ticket)

            return redirect(reverse('staff:flights'))
        except:
            return redirect(reverse('staff:flights'))


class CanceledFLightsListView(UserPassesTestMixin, ListView):
    template_name = 'canceled_flights_list.html'
    queryset = Flight.objects.filter(is_canceled=True).order_by('date')

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role == RoleOptions.supervisor.value

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CanceledFLightsListView, self).get_context_data()
        return context


class CheckInListView(UserPassesTestMixin, ListView):
    template_name = 'checkin_list.html'
    queryset = CheckIn.objects.filter(status=StatusOptions.in_progress.value)

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role in [RoleOptions.supervisor.value, RoleOptions.checkin_manager.value]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CheckInListView, self).get_context_data()
        return context


class CheckInView(UserPassesTestMixin, ProcessFormView):
    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role in [RoleOptions.supervisor.value, RoleOptions.checkin_manager.value]

    def get(self, request, pk):
        checkin = CheckIn.objects.get(id=pk)
        context = {'checkin': checkin,
                   'extra_luggage_price': checkin.ticket.flight.extra_luggage_price * checkin.extra_luggage}
        return render(request, 'checkin.html', context)

    def post(self, request, pk):
        checkin = CheckIn.objects.get(id=pk)
        checkin.status = StatusOptions.completed.value
        checkin.save()
        CreateBoardingPass.create_boarding_pass(checkin)
        try:
            no_checkin = CheckIn.objects.filter(ticket=checkin.ticket, status=StatusOptions.in_progress.value)[0]
        except:
            checkin.ticket.check_in = StatusOptions.completed.value
            checkin.ticket.save()
            boarding_passes_list = list(BoardingPass.objects.filter(ticket=checkin.ticket).all())
            email = checkin.ticket.passenger.user.email
            Emails.send_boarding_pass(request, boarding_passes_list, email)
        return redirect('staff:checkin list')


class GateListView(UserPassesTestMixin, ListView):
    template_name = 'gate_list.html'
    queryset = BoardingPass.objects.filter(status=StatusOptions.in_progress.value)

    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role in [RoleOptions.supervisor.value, RoleOptions.gate_manager.value]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GateListView, self).get_context_data()
        return context


class GateView(UserPassesTestMixin, ProcessFormView):
    def test_func(self):
        request_user_role = Staff.objects.get(user=self.request.user).role
        return request_user_role in [RoleOptions.supervisor.value, RoleOptions.gate_manager.value]

    def get(self, request, pk):
        boarding_pass = BoardingPass.objects.get(id=pk)
        context = {'boarding_pass': boarding_pass}
        return render(request, 'gate_approve.html', context)

    def post(self, request, pk):
        boarding_pass = BoardingPass.objects.get(id=pk)
        boarding_pass.status = StatusOptions.completed.value
        boarding_pass.save()
        try:
            not_registered = BoardingPass.objects.filter(ticket=boarding_pass.ticket,
                                                         status=StatusOptions.in_progress.value)[0]
        except:
            boarding_pass.ticket.gate_registration = StatusOptions.completed.value
            boarding_pass.ticket.save()
            email = boarding_pass.ticket.passenger.user.email
            Emails.seng_gate_register_confirmation(request, email)

        return redirect('staff:gate list')
















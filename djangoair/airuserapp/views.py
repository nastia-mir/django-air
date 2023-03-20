import json
import stripe

from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import ProcessFormView, View
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from airuserapp.forms import TicketForm, CheckInForm
from airuserapp.models import Ticket, CheckIn, BoardingPass, StatusOptions
from airuserapp.services import Emails

from airstaffapp.models import Flight, FlightDate, LunchOptions, LuggageOptions

from accounts.forms import EmailForm
from accounts.models import MyUser, Passenger
from accounts.services import PasswordGenerator

from djangoairproject import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(TemplateView):
    template_name = "home_passenger.html"

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()
        if self.request.user.is_authenticated:
            try:
                passenger = Passenger.objects.get(user=self.request.user)
                context['tickets'] = Ticket.objects.filter(passenger=passenger)
            except:
                context['tickets'] = None
            return context


class SearchTicketsView(CreateView):
    def get(self, request):
        context = {'form': TicketForm}
        return render(request, 'tickets.html', context)

    def post(self, request):
        destination = request.POST.get('destination')
        date = FlightDate.objects.get(date=request.POST.get('date'))

        passengers = request.POST.get('passengers')

        flight = Flight.objects.get(destination=destination, date=date, is_canceled=False)
        sold_tickets = Ticket.objects.filter(flight=flight).count()
        if int(passengers) <= flight.passengers - sold_tickets:
            ticket = Ticket.objects.create(flight=flight, tickets_quantity=passengers)
            return redirect(reverse('passengers:ticket details', args={ticket.id}))
        else:
            messages.error(request, 'No tickets available. Please, choose another flight.')
            return redirect('passengers:tickets')


# ajax
def load_dates(request):
    destination = request.GET.get('destination')
    flights = list(Flight.objects.filter(destination=destination, is_canceled=False))
    dates = [flight.date for flight in flights]
    context = {'dates': dates}
    return render(request, 'dates_dropdown.html', context)


class TicketDetailsView(UpdateView):
    template_name = 'ticket_details.html'
    model = Ticket
    fields = ['lunch', 'luggage']

    def get_context_data(self):
        context = super(TicketDetailsView, self).get_context_data()
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        context['ticket_price'] = ticket.flight.ticket_price * ticket.tickets_quantity
        context['lunch_options'] = ticket.flight.lunch.all()
        context['luggage_options'] = ticket.flight.luggage.all()
        context['ticket'] = ticket
        return context

    def post(self, request, pk):
        lunch = request.POST.get('lunch')
        luggage = request.POST.get('luggage')
        ticket = Ticket.objects.get(id=pk)
        if not ticket:
            ticket = Ticket.objects.get(id=pk)
        ticket.lunch = LunchOptions.objects.get(description=lunch.split(',')[0])
        luggage_options = {
            'No luggage': '0',
            'One luggage': '1',
            'Two luggage': '2'
        }
        ticket.luggage = LuggageOptions.objects.get(quantity=luggage_options[luggage.split(',')[0]])
        ticket.save()
        return redirect(reverse('passengers:ticket booking', args={pk}))


class TicketBookingView(UpdateView):

    def get(self, request, pk):
        context = {'form': EmailForm}
        ticket = Ticket.objects.get(id=pk)
        context['ticket'] = ticket
        total_price = (ticket.flight.ticket_price + ticket.lunch.price + ticket.luggage.price) * ticket.tickets_quantity
        context['total_price'] = total_price
        if request.user.is_authenticated and not request.user.is_airlines_staff:
            context['user'] = request.user
        else:
            context['user'] = None
        return render(request, 'ticket_booking.html', context)

    def post(self, request, pk):
        email_form = EmailForm(request.POST)
        ticket = Ticket.objects.get(id=pk)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            try:
                existing_user = MyUser.objects.get(email=email)
                existing_passenger, created = Passenger.objects.get_or_create(user=existing_user)
                ticket.passenger = existing_passenger
                ticket.save()
            except:
                password = PasswordGenerator.generate_password()
                user = MyUser.objects.create_user(email=email, password=password)
                passenger_account = Passenger.objects.create(user=user)
                passenger_account.save()
                ticket.passenger = passenger_account
                ticket.save()
                Emails.send_temporary_password(request, email, password)

            Emails.send_ticket_details(request, email, ticket)
        else:
            messages.error(request, 'Please enter valid email')
            return redirect(reverse('passengers:ticket booking', args={pk}))

        return redirect(reverse('passengers:home'))


class ViewTicketView(TemplateView):
    template_name = 'view_ticket.html'

    def get_context_data(self, pk):
        context = super(ViewTicketView, self).get_context_data()
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        context['ticket'] = ticket
        total_price = (ticket.flight.ticket_price + ticket.lunch.price + ticket.luggage.price) * ticket.tickets_quantity
        context['total_price'] = total_price
        return context


class ProcessPaymentView(View):

    def post(self, request, pk, price):
        customer = stripe.Customer.create(
            email=request.user.email,
            source=request.POST.get('stripeToken')
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=price * 100,
            currency='usd',
            description='Ticket payment',
        )
        ticket = Ticket.objects.get(id=pk)
        ticket.is_paid = True

        return redirect(reverse('passengers:view ticket', args={pk}))


class CheckInView(ProcessFormView):
    def get(self, request, pk):
        ticket = Ticket.objects.get(id=pk)
        context = {}
        if ticket.check_in in [StatusOptions.waiting_for_approval.value, StatusOptions.completed.value]:
            context['check_in'] = True
        else:
            context['ticket'] = ticket
            checkins = list(CheckIn.objects.filter(ticket=ticket))
            if checkins:
                context['passengers'] = checkins
                if len(checkins) < ticket.tickets_quantity:
                    context['form'] = CheckInForm
                    context['left'] = ticket.tickets_quantity - len(checkins)
                elif len(checkins) == ticket.tickets_quantity:
                    context['form'] = None
                    context['left'] = 0
                else:
                    context['form'] = None
                    context['left'] = -1
            else:
                context['passengers'] = None
                context['form'] = CheckInForm
                context['left'] = ticket.tickets_quantity

            return render(request, 'passenger_checkin.html', context)

    def post(self, request, pk):
        ticket = Ticket.objects.get(id=pk)
        if 'add_passenger' in request.POST:
            form = CheckInForm(request.POST)
            if form.is_valid():
                checkin_form = form.save(commit=False)
                checkin_form.ticket = ticket
                checkin_form.save()
                if ticket.check_in != StatusOptions.editing.value:
                    ticket.check_in = StatusOptions.editing.value
                    ticket.save()
            else:
                messages.error(request, 'Please enter valid data.')
            return redirect(reverse('passengers:checkin', args={pk}))
        elif 'checkin' in request.POST:
            ticket.check_in = StatusOptions.waiting_for_approval.value
            ticket.save()
            return redirect(reverse('passengers:view ticket', args={pk}))


class DeleteFromCheckin(DeleteView):
    def get(self, request, pk):
        checkin = CheckIn.objects.get(id=self.kwargs['pk'])
        checkin.delete()
        return redirect(reverse('passengers:checkin', args={checkin.ticket.id}))


class GateRegisterView(ProcessFormView):
    def get(self, request, pk):
        ticket = Ticket.objects.get(id=pk)
        context = {'boarding_passes_list': list(BoardingPass.objects.filter(ticket=ticket))}
        return render(request, 'gate_register.html', context)

    def post(self, request, pk):
        ticket = Ticket.objects.get(id=pk)
        for boarding_pass in list(BoardingPass.objects.filter(ticket=ticket)):
            boarding_pass.status = StatusOptions.in_progress.value
            boarding_pass.save()
        ticket.gate_registration = StatusOptions.waiting_for_approval.value
        ticket.save()
        return redirect(reverse('passengers:view ticket', args={pk}))

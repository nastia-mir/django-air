from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from airuserapp.forms import TicketForm, PassengerNameForm
from airuserapp.models import Ticket, CheckIn, PassengerName
from airuserapp.services import Emails

from airstaffapp.models import Flight, FlightDate, LunchOptions, LuggageOptions

from accounts.forms import EmailForm
from accounts.models import MyUser, Passenger
from accounts.services import PasswordGenerator


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
        sold_tickets = len(Ticket.objects.filter(flight=flight).all())
        if int(passengers) <= flight.passengers-sold_tickets:
            ticket = Ticket.objects.create(flight=flight, tickets_quantity=passengers)
            return redirect(reverse('passengers:ticket details', args={ticket.id}))
        else:
            messages.error(request, 'No tickets available. Please, choose another flight.')
            return redirect('passengers:tickets')


#ajax
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
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
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
        return context


class CheckInView(ProcessFormView):
    def get(self, request, pk):
        context = {}
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        context['ticket'] = ticket
        checkin, created = CheckIn.objects.get_or_create(ticket=ticket)
        print(checkin.passengers.all())
        if not created and checkin.passengers.all():

            context['passengers'] = checkin.passengers.all()
            if checkin.passengers.count() < ticket.tickets_quantity:
                context['form'] = PassengerNameForm
                context['left'] = ticket.tickets_quantity - checkin.passengers.count()
            elif checkin.passengers.count() == ticket.tickets_quantity:
                context['form'] = None
                context['left'] = 0
            else:
                context['form'] = None
                context['left'] = -1

        else:
            context['passengers'] = None
            context['form'] = PassengerNameForm
            context['left'] = ticket.tickets_quantity

        return render(request, 'passenger_checkin.html', context)

    def post(self, request, pk):
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        checkin = CheckIn.objects.get(ticket=ticket)
        if 'add_passenger' in request.POST:
            form = PassengerNameForm(request.POST)
            if form.is_valid():
                name_form = form.save(commit=False)
                print(name_form)
                name_form.save()
                checkin.passengers.add(name_form)
                return redirect(reverse('passengers:checkin', args={pk}))
        elif 'checkin' in request.POST:
            checkin.status = 'in_progress'
            checkin.save()
            ticket.check_in = True
            ticket.save()
            return redirect(reverse('passengers:view ticket', args={pk}))


class DeleteFromCheckin(DeleteView):
    def get(self, request, pk, passenger_pk):
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        checkin = CheckIn.objects.get(ticket=ticket)
        passenger = PassengerName.objects.get(id=self.kwargs['passenger_pk'])
        checkin.passengers.remove(passenger)
        return redirect(reverse('passengers:checkin', args={pk}))













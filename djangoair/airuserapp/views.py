from django.views.generic import TemplateView, UpdateView, CreateView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from airuserapp.forms import TicketForm
from airstaffapp.models import Flight, FlightDate, LunchOptions, LuggageOptions
from airuserapp.models import Ticket


class HomeView(TemplateView):
    template_name = "home_user.html"


class SearchTicketsView(CreateView):
    def get(self, request):
        context = {'form': TicketForm}
        return render(request, 'tickets.html', context)

    def post(self, request):
        destination = request.POST.get('destination')
        date = FlightDate.objects.get(date=request.POST.get('date'))

        passengers = request.POST.get('passengers')

        flight = Flight.objects.get(destination=destination, date=date)
        sold_tickets = len(Ticket.objects.filter(flight=flight).all())
        if int(passengers) <= flight.passengers-sold_tickets:
            Ticket.objects.create(flight=flight, tickets_quantity=passengers)
            return redirect(reverse('passengers:ticket details'))
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
    pass








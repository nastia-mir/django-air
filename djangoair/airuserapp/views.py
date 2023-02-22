from django.views.generic import TemplateView, UpdateView, CreateView, FormView
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from airuserapp.forms import TicketForm
from airstaffapp.models import Flight, FlightDate
from airuserapp.models import Ticket


class HomeView(TemplateView):
    template_name = "home_user.html"


class SearchTicketsView(View):
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
            return redirect('tickets')


#ajax
def load_dates(request):
    destination = request.GET.get('destination')
    flights = list(Flight.objects.filter(destination=destination, is_canceled=False))
    dates = [flight.date for flight in flights]
    context = {'dates': dates}
    return render(request, 'dates_dropdown.html', context)


class TicketDetailsView(UpdateView):
    pass







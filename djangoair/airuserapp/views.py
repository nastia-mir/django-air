from django.views.generic import TemplateView, UpdateView, CreateView, FormView
from django.views import View
from django.shortcuts import render, redirect, reverse

from airuserapp.forms import TicketForm
from airstaffapp.models import Flight


class HomeView(TemplateView):
    template_name = "home_user.html"


class SearchTicketsView(View):
    def get(self, request):
        context = {'form': TicketForm}
        return render(request, 'tickets.html', context)

    def post(self, request):
        pass


#ajax
def load_dates(request):
    destination = request.GET.get('destination')
    flights = list(Flight.objects.filter(destination=destination))
    dates = [flight.date for flight in flights]
    context = {'dates': dates}
    return render(request, 'dates_dropdown.html', context)







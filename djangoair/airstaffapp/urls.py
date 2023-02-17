from django.urls import path
from django.contrib.auth.decorators import login_required

from airstaffapp import views

urlpatterns = [
    path('',  login_required(views.HomeView.as_view()), name='home'),
    path('staff_list/', login_required(views.StaffListView.as_view()), name='staff list'),
    path('staff_list/<pk>/', login_required(views.EditRoleView.as_view()), name='edit role'),

    path('flights/', login_required(views.FlightsView.as_view()), name='flights'),
    path('flights/create', login_required(views.CreateFlightView.as_view()), name='create flight'),
    path('flights/<pk>/edit', login_required(views.EditFlightView.as_view()), name='edit flight options'),
    path('flights/<pk>/cancel', login_required(views.CancelFlightView.as_view()), name='cancel flight'),



]
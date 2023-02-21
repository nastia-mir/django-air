from django.urls import path
from airuserapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('tickets/', views.SearchTicketsView.as_view(), name='tickets'),
    #path('tickets/details/', views.TicketDetailsView.as_view(), name='ticket details'),
    #path('tickets/booking/', views.TicketBookingView.as_view(), name='ticket booking'),

    path('ajax/load_dates/', views.load_dates, name='ajax load dates'),

]
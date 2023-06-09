from django.urls import path
from django.contrib.auth.decorators import login_required

from airuserapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('tickets/', views.SearchTicketsView.as_view(), name='tickets'),
    path('tickets/<pk>/details/', views.TicketDetailsView.as_view(), name='ticket details'),
    path('tickets/<pk>/booking/', views.TicketBookingView.as_view(), name='ticket booking'),

    path('payment/<pk>/ticket/<int:price>/', views.ProcessTicketPaymentView.as_view(), name='ticket payment'),
    path('payment/<pk>/luggage/<int:price>/', views.ProcessExtraLuggagePaymentView.as_view(), name='extra luggage payment'),
    path('refund/<pk>/', views.RefundView.as_view(), name='refund'),

    path('ajax/load_dates/', views.load_dates, name='ajax load dates'),

    path('view_ticket/<pk>/', login_required(views.ViewTicketView.as_view()), name='view ticket'),
    path('checkin/<pk>/', login_required(views.CheckInView.as_view()), name='checkin'),
    path('checkin/delete/<pk>/', login_required(views.DeleteFromCheckin.as_view()), name='delete checkin'),

    path('gate/<pk>/', login_required(views.GateRegisterView.as_view()), name='gate register'),

]
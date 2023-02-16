from django.urls import path
from airstaffapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('staff_list/', views.StaffListView.as_view(), name='staff list'),
    path('staff_list/<pk>/', views.EditRoleView.as_view(), name='edit role'),

    path('flights/', views.FlightsView.as_view(), name='flights'),
    path('flights/create', views.CreateFlightView.as_view(), name='create flight'),
    path('flights/<pk>/edit', views.EditFlightView.as_view(), name='edit flight option'),
    path('flights/<pk>/cancel', views.CancelFlightView.as_view(), name='cancel flight'),



]
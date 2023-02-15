from django.urls import path
from airstaffapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

]
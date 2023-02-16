from django.urls import path
from airuserapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

]
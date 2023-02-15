from django.urls import path
from airstaffapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('staff_list/', views.StaffListView.as_view(), name='staff list'),
    path('staff_list/<pk>', views.EditRoleView.as_view(), name='edit role'),

]
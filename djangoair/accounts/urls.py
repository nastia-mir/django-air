from django.urls import path
from django.contrib.auth.decorators import login_required

from accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', login_required(views.EditProfileView.as_view()), name='edit profile'),
    path('change_password/', login_required(views.ChangePasswordView.as_view()), name='change password'),
    path('restore_password/', views.RestorePasswordView.as_view(), name='restore password'),
]

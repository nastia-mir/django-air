
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/', include(('airstaffapp.urls', 'staff'), namespace='staff')),
    path('passengers/', include(('airuserapp.urls', 'passengers'), namespace='passengers')),
    path('', include(('accounts.urls', 'accounts'), namespace='accounts')),
]

from django.contrib import admin
from .models import MyUser, Passenger, Staff

admin.site.register(MyUser)
admin.site.register(Passenger)
admin.site.register(Staff)

from django.contrib import admin
from accounts.models import MyUser, Passenger, Staff

admin.site.register(MyUser)
admin.site.register(Passenger)
admin.site.register(Staff)

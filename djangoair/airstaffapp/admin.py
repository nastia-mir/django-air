from django.contrib import admin
from airstaffapp.models import Flight, LunchOptions, LuggageOptions, FlightDate, CheckIn

admin.site.register(Flight)
admin.site.register(LunchOptions)
admin.site.register(LuggageOptions)
admin.site.register(FlightDate)
admin.site.register(CheckIn)
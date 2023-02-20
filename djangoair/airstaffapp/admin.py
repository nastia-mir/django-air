from django.contrib import admin
from airstaffapp.models import Flight, LunchOptions, LuggageOptions

admin.site.register(Flight)
admin.site.register(LunchOptions)
admin.site.register(LuggageOptions)
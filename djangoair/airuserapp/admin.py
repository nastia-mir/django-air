from django.contrib import admin

from airuserapp.models import Ticket, CheckIn, BoardingPass, PassengerName

admin.site.register(Ticket)
admin.site.register(CheckIn)
admin.site.register(BoardingPass)
admin.site.register(PassengerName)

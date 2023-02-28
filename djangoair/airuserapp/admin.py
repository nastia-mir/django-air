from django.contrib import admin

from airuserapp.models import Ticket, CheckIn, BoardingPass

admin.site.register(Ticket)
admin.site.register(CheckIn)
admin.site.register(BoardingPass)

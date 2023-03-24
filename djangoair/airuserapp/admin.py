from django.contrib import admin

from airuserapp.models import Ticket, CheckIn, BoardingPass, PassengerFullName, ExtraLuggageTicket, TicketBill, \
    ExtraLuggageBill, RefundBill

admin.site.register(Ticket)
admin.site.register(CheckIn)
admin.site.register(BoardingPass)
admin.site.register(PassengerFullName)
admin.site.register(ExtraLuggageTicket)
admin.site.register(TicketBill)
admin.site.register(ExtraLuggageBill)
admin.site.register(RefundBill)
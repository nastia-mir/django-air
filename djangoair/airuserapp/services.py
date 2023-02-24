from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages

from djangoairproject.settings import EMAIL_HOST_USER


class Emails:
    @classmethod
    def send_temporary_password(cls, request, email, password):
        subject = 'Your temporary password'
        message = render_to_string("emails/temp_password.txt", {
            'password': password
        })
        email = send_mail(subject, message, EMAIL_HOST_USER, [email, EMAIL_HOST_USER])
        if email:
            messages.success(request, 'We send you a temporary password. Please, check your email.')
        else:
            messages.error(request, "We couldn't send you an email, please check if you typed it correctly.")

    @classmethod
    def send_ticket_details(cls, request, email, ticket):
        context = {'ticket': ticket}
        total_price = ticket.flight.ticket_price * ticket.tickets_quantity + ticket.lunch.price + ticket.luggage.price
        context['total_price'] = total_price

        subject = 'Django Air tickets'
        message = render_to_string("emails/tickets_info.txt", context)
        email = send_mail(subject, message, EMAIL_HOST_USER, [email, EMAIL_HOST_USER])
        if email:
            messages.success(request, 'Your tickets is available at your email and in personal cabinet.')
        else:
            messages.error(request, "We couldn't send you an email, please check if you typed it correctly.")
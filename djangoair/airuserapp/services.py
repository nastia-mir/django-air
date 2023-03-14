from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from djangoairproject.settings import EMAIL_HOST_USER

from accounts.tokens import account_activation_token


class Emails:
    @classmethod
    def send_flight_cancellation_info(cls, request, flight, ticket):
        refund = ticket.flight.ticket_price * ticket.tickets_quantity + ticket.lunch.price + ticket.luggage.price
        passenger_email = ticket.passenger.user.email
        context = {'flight': flight,
                   'refund': refund}
        subject = 'Django Air: Flight cancellation'
        message = render_to_string("emails/flight_cancellation.txt", context)
        email = send_mail(subject, message, EMAIL_HOST_USER, [passenger_email])
        if email:
            messages.success(request, 'Email if sent.')
        else:
            messages.error(request, "Email is not sent.")

    @classmethod
    def send_ticket_details(cls, request, email, ticket):
        context = {'ticket': ticket}
        total_price = ticket.flight.ticket_price * ticket.tickets_quantity + ticket.lunch.price + ticket.luggage.price
        context['total_price'] = total_price

        subject = 'Django Air: Tickets'
        message = render_to_string("emails/tickets_info.txt", context)
        email = send_mail(subject, message, EMAIL_HOST_USER, [email])
        if email:
            messages.success(request, 'Your tickets is available at your email and in personal cabinet.')
        else:
            messages.error(request, "We couldn't send you an email, please check if you typed it correctly.")

    @classmethod
    def send_boarding_pass(cls, request, boarding_passes_list, email):
        context = {
            'boarding_passes_list': boarding_passes_list
        }

        subject = 'Django Air: Boarding Passes'
        message = strip_tags(render_to_string("emails/boarding_passes.html", context))
        email = send_mail(subject, message, EMAIL_HOST_USER, [email])
        if email:
            messages.success(request, 'Boarding passes are sent.')
        else:
            messages.error(request, "Boarding passes are  not sent.")

    @classmethod
    def send_extra_luggage_bill(cls, request, extra_luggage_passes, email):
        context = {
            'extra_luggage_passes': extra_luggage_passes
        }

        subject = 'Django Air: Extra luggage bill'
        message = render_to_string("emails/extra_luggage_bill.txt", context)
        email = send_mail(subject, message, EMAIL_HOST_USER, [email])
        if email:
            messages.success(request, 'Extra luggage bills is sent.')
        else:
            messages.error(request, "Extra luggage bill is not sent.")

    @classmethod
    def seng_gate_register_confirmation(cls, request, email):
        subject = 'Django Air: Successfully registered for a flight'
        message = render_to_string("emails/register_confirmation.txt")
        email = send_mail(subject, message, EMAIL_HOST_USER, [email])
        if email:
            messages.success(request, 'Register confirmation email is sent.')
        else:
            messages.error(request, "Register confirmation email is not sent.")

    @classmethod
    def send_password_resetting_link(cls, request, user):
        subject = 'Django Air: reset password'
        message = render_to_string("emails/change_password.txt", {
            'user': user,
            'domain': get_current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        })
        email = send_mail(subject, message, EMAIL_HOST_USER, [user.email])
        if email:
            messages.success(request, 'We send you a link to change password via email.')
        else:
            messages.error(request, "We couldn't send you an email, please check if you typed it correctly.")

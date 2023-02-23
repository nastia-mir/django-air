from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages

from djangoairproject.settings import EMAIL_HOST_USER


class Emails:
    @classmethod
    def send_temporary_password(cls, request, email, password):
        subject = 'Your temporary password'
        message = render_to_string("emails/temp_password_email.txt", {
            'password': password
        })
        email = send_mail(subject, message, EMAIL_HOST_USER, [email])
        if email:
            messages.success(request, 'We send you a email to complete the registration.')
        else:
            messages.error(request, "We couldn't send you an email, please check if you typed it correctly.")
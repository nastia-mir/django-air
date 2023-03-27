from django.utils.crypto import get_random_string

from airuserapp.models import BoardingPass


class CreateBoardingPass:
    @classmethod
    def create_boarding_pass(cls, checkin):
        if checkin.status == 'completed':
            chars = 'ABCDEFGHIJKLMNOPQRSTUVXXYZ0123456789'
            code = get_random_string(10, chars)
            boarding_pass = BoardingPass.objects.create(ticket=checkin.ticket,
                                                        passenger=checkin.passenger,
                                                        code=code,
                                                        extra_luggage=checkin.extra_luggage)
            boarding_pass.save()
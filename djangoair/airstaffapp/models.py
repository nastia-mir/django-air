from django.db import models


class FlightOptions(models.Model):
    lunch = models.BooleanField(default=True)
    lunch_price = models.IntegerField(blank=False, null=False)
    luggage_options = (
        ('0', 'No luggage'),
        ('1', 'One luggage'),
        ('2', 'Two luggage')
    )
    luggage = models.CharField(max_length=50, choices=luggage_options)
    luggage_price = models.IntegerField(blank=False, null=False)

    objects = models.Manager()

    def __str__(self):
        if self.lunch:
            return '{}, lunch available.'.format(self.get_luggage_display())
        if self.lunch:
            return '{}, lunch not available.'.format(self.get_luggage_display())


class Flight(models.Model):
    destinations = (
        ('lisbon', 'Lisbon, Portugal'),
        ('tokio', 'Tokio, Japan'),
        ('nairobi', 'Nairobi, Kenya'),
        ('rio_de_janeiro', 'Rio de Janeiro, Brazil'),
        ('helsinki', 'Helsinki, Finland'),
        ('denver', 'Denver, USA'),
        ('oslo', 'Oslo, Norway'),
        ('berlin', 'Berlin, Germany'),
        ('stockholm', 'Stockholm, Sweden'),
        ('marseille', 'Marseille, France'),
        ('bogota', 'Bogota, Columbia'),
        ('palermo', 'Palermo, Italy')
    )
    destination = models.CharField(max_length=500, choices=destinations)
    date = models.DateField(auto_now=False, auto_now_add=False)
    passengers = models.IntegerField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    flight_options = models.OneToOneField(FlightOptions, on_delete=models.CASCADE,  related_name="flight_options")

    # is_completed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        if self.is_canceled:
            return 'Destination: {}; date: {}. Canceled.'.format(self.destination, self.date)
        else:
            return 'Destination: {}; date: {}'.format(self.destination, self.date)
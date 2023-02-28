from django.db import models


class LunchOptions(models.Model):
    description = models.CharField(max_length=500)
    price = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return '{}, price {}$'.format(self.description, self.price)


class LuggageOptions(models.Model):
    quantity_options = (
        ('0', 'No luggage'),
        ('1', 'One luggage'),
        ('2', 'Two luggage')
    )
    quantity = models.CharField(max_length=150, choices=quantity_options)
    price = models.IntegerField(blank=False, null=False)

    objects = models.Manager()

    def __str__(self):
        return '{}, price {}$'.format(self.get_quantity_display(), self.price)


class FlightDate(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)

    objects = models.Manager()

    def __str__(self):
        return str(self.date)


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
    date = models.ForeignKey(FlightDate, on_delete=models.CASCADE, related_name='flight_date')
    passengers = models.IntegerField(blank=False, null=False)
    ticket_price = models.IntegerField(blank=False, null=False)
    lunch = models.ManyToManyField(LunchOptions, related_name='lunch_pool')
    luggage = models.ManyToManyField(LuggageOptions, related_name='luggage_pool')
    extra_luggage_price = models.IntegerField(default=50)

    is_canceled = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        if self.is_canceled:
            return '{}, {}. Canceled.'.format(self.get_destination_display(), self.date.date)
        else:
            return '{}, {}.'.format(self.get_destination_display(), self.date.date)





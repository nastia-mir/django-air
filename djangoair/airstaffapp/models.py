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
    lunch = models.ManyToManyField(LunchOptions, related_name='lunch')
    luggage = models.ManyToManyField(LuggageOptions, related_name='luggage')

    # is_completed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        if self.is_canceled:
            return 'Destination: {}; date: {}. Canceled.'.format(self.destination, self.date)
        else:
            return 'Destination: {}; date: {}'.format(self.destination, self.date)

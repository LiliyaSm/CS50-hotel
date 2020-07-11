from django.db import models

# Create your models here.


class Booking(models.Model):

    arrival = models.DateField('arrival')
    departure = models.DateField('departure')

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator
from datetime import date
from django.contrib.auth.models import User
from decimal import Decimal

GUESTS_CHOICES = (
       (1, 1),
       (2, 2),
       (3, 3),
       (4, 4),
   )
# upload_location = FileSystemStorage(location='/reservations/static/img')
upload_path = 'roomFotos'

class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", null=False)
    confirmed = models.BooleanField(default=False)


class RoomFacility(models.Model):
    item = models.CharField(max_length=100)  # symmetrical = False,

    def __str__(self):
        return f"{self.item}"

    class Meta:
       verbose_name = 'Room Facility'
       verbose_name_plural = 'Room Facilities'


class RoomCategory(models.Model):
    CATEGORY_CHOICES = (
        ('Single', 'Single'),
        ('Double', 'Double/twin'),
        ('Superior', 'Superior'),
        ('Suite', 'Suite'),
        ('SPA', 'Suite SPA'),
    )

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=1000, blank=True)
    # the upload_to option to specify a subdirectory of MEDIA_ROOT to use for uploaded files
    mainFoto = models.ImageField(upload_to=upload_path, blank=True, null=True)
    facilities = models.ManyToManyField(RoomFacility)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    capacity = models.PositiveIntegerField(choices=GUESTS_CHOICES, default=1)
    totalAmount = models.PositiveIntegerField(default=1)

    # items = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Room category'
        verbose_name_plural = 'Room categories'

class Room(models.Model):

    roomNumber = models.CharField(max_length=3)
    category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.roomNumber} {self.category}"


class Booking(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='ordered_room')

    arrival = models.DateField('arrival',
                               validators=[MinValueValidator(limit_value=date.today)])
    departure = models.DateField('departure',
                                 validators=[MinValueValidator(limit_value=date.today)])
    # people per room
    guests = models.PositiveIntegerField(
        choices=GUESTS_CHOICES, default=1, verbose_name='guests per room')

    calc_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal(0))




class RoomImage(models.Model):
    room = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to=upload_path, blank=True, null=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} image"

from django.db import models
from django.core.files.storage import FileSystemStorage

# upload_location = FileSystemStorage(location='/reservations/static/img')
upload_path = 'roomFotos'
class Booking(models.Model):

    arrival = models.DateField('arrival')
    departure = models.DateField('departure')


class RoomFacility(models.Model):
    item = models.CharField(max_length=100)  # symmetrical = False,

    def __str__(self):
        return f"{self.item}"

    class Meta:
       verbose_name = 'RoomFacility'
       verbose_name_plural = 'RoomFacilities'




class Room(models.Model):
    CATEGORY_CHOICES = (
        ('Single', 'Single'),
        ('Double', 'Double/twin'),
        ('Superior', 'Superior'),
        ('Suite', 'Suite'),
        ('SPA', 'Suite SPA'),
    )

    GUESTS_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )
    roomNumber = models.CharField(max_length=3)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=1000, blank=True)
    # the upload_to option to specify a subdirectory of MEDIA_ROOT to use for uploaded files
    
    facilities = models.ManyToManyField(RoomFacility)
    price = models.DecimalField(max_digits=6, decimal_places=2)    
    guests = models.PositiveIntegerField(choices=GUESTS_CHOICES, default=1)
    totalAmount = models.PositiveIntegerField(default=1)


    # items = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.category}"


class Image(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to=upload_path, blank=True, null=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)

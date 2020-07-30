
from django.contrib import admin
from .models import Room, RoomFacility, RoomImage, RoomCategory, Booking, Transfer
from django.db import models

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 3


class RoomCategoryAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline, ]


class TransferAdmin (admin.TabularInline):
    model = Transfer

class BookingAdmin(admin.ModelAdmin):
    inlines = [TransferAdmin, ]
    # filter by user name and order number
    search_fields = (
        "user__username", "id"
    )

admin.site.register(RoomCategory, RoomCategoryAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Room)
admin.site.register(RoomFacility)

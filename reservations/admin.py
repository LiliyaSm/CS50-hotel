
from django.contrib import admin
from .models import Room, RoomFacility, Image
from django.db import models


# class ItemInline(admin.TabularInline):
#     model = Room
#     # no need extra forms for adding new item orders
#     extra = 0
#     filter_horizontal = ('id',)

    # class Media:
    #     css = {
    #         'all': ('css/style.css',),
    #     }


admin.site.register(Room)
admin.site.register(RoomFacility)
admin.site.register(Image)

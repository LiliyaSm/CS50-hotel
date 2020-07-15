
from django.contrib import admin
from .models import Room, RoomFacility, RoomImage, RoomCategory
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


# admin.py
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 3


class RoomCategoryAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline, ]


admin.site.register(RoomCategory, RoomCategoryAdmin)

# admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(RoomFacility)
# admin.site.register(RoomImage)

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
# from django.db.models import Q
from django.http import HttpResponse
from .models import Booking, Room, RoomCategory
# import json
# import decimal
import datetime
from django.views.generic.list import ListView
from django.contrib import messages
from django import forms

now = str(datetime.date.today())
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'arrival': forms.DateInput(attrs={'type': 'date', "value": now, "min": now}),
            'departure': forms.DateInput(attrs={'type': 'date', "value": now, "min": now})
        }


def index(request):
    """rendering items on the main page"""

    if request.method == "GET":
        # items = Item.objects.exclude(
        #     Q(group__dishType="Toppings") | Q(group__dishType="Extras"))
        return render(request, "reservations/index.html", {
            "form": BookingForm()
        })
    if request.method == "POST":
        return redirect("booking")


def booking(request):
    return render(request, "reservations/booking.html")


def rooms(request):
    rooms = RoomCategory.objects.all()
    return render(request, "reservations/rooms.html", {
        "rooms": rooms,
    })

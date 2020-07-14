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
from django.views.generic import DetailView
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


class CategoryListView(ListView):

    # Add in a QuerySet of all the categories
    queryset = RoomCategory.objects.all()
    template_name = 'reservations/rooms.html'


class CategoryDetail(DetailView):

    context_object_name = 'category'
    queryset = RoomCategory.objects.all()
    slug_field = 'category'
    template_name = "reservations/room-detail.html"
    slug_url_kwarg = 'category'


def index(request):
    """rendering items on the main page"""

    if request.method == "GET":
        return render(request, "reservations/index.html", {
            "form": BookingForm()
        })
    if request.method == "POST":
        return redirect("booking")


def booking(request):
    return render(request, "reservations/booking.html")


# def rooms(request):
#     rooms = RoomCategory.objects.all()
#     return render(request, "reservations/rooms.html", {
#         "rooms": rooms,
#     })

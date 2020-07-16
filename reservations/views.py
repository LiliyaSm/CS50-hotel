from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
# from django.db.models import Q
from django.http import HttpResponse
from .models import Booking, Room, RoomCategory, RoomImage
# import json
# import decimal
import datetime
from django.views.generic.list import ListView
from django.views.generic import DetailView, View
from django.contrib import messages
from django import forms


now = str(datetime.date.today())


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('arrival', 'departure')
        widgets = {
            'arrival': forms.DateInput(attrs={'type': 'date', "value": now, "min": now }),
            'departure': forms.DateInput(attrs={'type': 'date', "value": now, "min": now}),
        }


class BookingExtentedForm(BookingForm):
    class Meta(BookingForm.Meta):
        fields = '__all__'


class CategoryListView(ListView):

    # Add in a QuerySet of all the categories
    queryset = RoomCategory.objects.all()
    template_name = 'reservations/rooms.html'


class CategoryDetail(DetailView):

    context_object_name = 'category'
    queryset = RoomCategory.objects.all()
    slug_field = 'category'
    slug_url_kwarg = 'category'
    template_name = "reservations/room-detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['images'] = RoomImage.objects.filter(room=self.object)
        return context


class IndexView(View):

    template_name = 'reservations/index.html'
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        # form =  ClockOutForm(instance=TimesheetEntry.objects.get(id=pk))
        form = BookingForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

#       form.save()
        return redirect("booking")

# def index(request):
#     """rendering items on the main page"""

#     if request.method == "GET":
#         return render(request, "reservations/index.html", {
#             "form": BookingForm()
#         })
#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if not form.is_valid():
#             return render(request, "reservations/index.html", {
#                 "form": BookingForm()
#             })
#         arrival = form.cleaned_data["arrival"]
#         departure = form.cleaned_data["departure"]
#         return redirect("booking")


def booking(request):
    return render(request, "reservations/booking.html", {
        "form": BookingExtentedForm()
    })


# def rooms(request):
#     rooms = RoomCategory.objects.all()
#     return render(request, "reservations/rooms.html", {
#         "rooms": rooms,
#     })

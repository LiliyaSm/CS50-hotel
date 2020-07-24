from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
# from django.db.models import Q
from django.http import HttpResponse
from .models import Booking, Room, RoomCategory, RoomImage, Transfer
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from django.views.generic.list import ListView
from django.views.generic import DetailView, View
from django.contrib import messages
from django import forms
from django.http import JsonResponse

now = str(datetime.date.today())

def deserialize(data):
    return json.dumps(
        data,
        sort_keys=True,
        indent=1,
        cls=DjangoJSONEncoder
    )

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('arrival', 'departure', "guests")
        widgets = {
            'arrival': forms.DateInput(attrs={'type': 'date', "value": now, "min": now }),
            'departure': forms.DateInput(attrs={'type': 'date', "value": now, "min": now}),
        }


class TransferForm(forms.ModelForm):
    class Meta:

        model = Transfer
        fields = ("__all__")
        help_texts = {
            "flightNumber": "Including letters and digits"
        }
        labels = {
            'flightNumber': "Flight number",
            'arrivalDate': "Arrival date",
            'arrivalTime': "Arrival time",
            'airlineCompany': "Airline company",
            "additionalInformation": "Additional information"
        }
        widgets = {
            'arrivalDate': forms.DateInput(attrs={'type': 'date', "value": now, "min": now}),
            "arrivalTime": forms.TimeInput(attrs={'type': 'time'}, format='%H:%M %p',),
            "additionalInformation": forms.Textarea(attrs={'class': 'form-control', "rows": "5"},)
        }

class CategoryListView(ListView):

    # Add in a QuerySet of all the categories
    queryset = RoomCategory.objects.all()
    template_name = 'reservations/rooms.html'


class CategoryDetail(DetailView):

    context_object_name = 'name'
    queryset = RoomCategory.objects.all()
    slug_field = 'name'
    slug_url_kwarg = 'name'
    template_name = "reservations/room-detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['images'] = RoomImage.objects.filter(room=self.object)
        return context


class IndexView(View):
    """rendering items on the main page"""
    template_name = 'reservations/index.html'
    form = BookingForm()
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    # request.session["arrival"] = form.cleaned_data["arrival"]
    # request.session["departure"] = form.cleaned_data["departure"]

class BookingView(View):

    template_name = "reservations/booking.html"

    def get(self, request, *args, **kwargs):
        form = BookingForm(request.GET)
        transferForm = TransferForm()
        if not form.is_valid():

        #come by nav link and form is empty
            try:
                data = eval(request.session.get('form_data'))
                form = BookingForm(initial=data)
                # make search
                number_of_guests = int(form.initial["guests"])
                available_rooms = RoomCategory.objects.filter(
                    capacity__gte=number_of_guests)
                return render(request, self.template_name, {
                    "form": form, "available_rooms": available_rooms
            })

            except TypeError:
                #if form empty display all available rooms (first search)
                form = BookingForm()
                available_rooms = RoomCategory.objects.all()
                return render(request, self.template_name, {
                    "form": form, "available_rooms": available_rooms
            })

        # case - come from index
        available_rooms = RoomCategory.objects.all()        
        # save user search
        request.session['form_data'] = deserialize(form.cleaned_data)

        return render(request, self.template_name, {'form': form, "available_rooms": available_rooms, "transferForm": transferForm})


    def post(self, request, *args, **kwargs):
        available_rooms = RoomCategory.objects.all()

        return render(request, self.template_name, {
            "form": form, "available_rooms": available_rooms
        })
        




    # arrival = request.GET['arrival']
    # arrival = request.GET.get('arrival')


def booking_submit(request):
    """ returns response with list of available categories' ids  """

    arrival = request.GET.get("arrival", "")
    departure = request.GET.get("departure", "")
    number_of_guests = int(request.GET.get("guests", ""))

    # flat = True to get a plain list instead of a list of tuples
    categories = RoomCategory.objects.filter(
        capacity__gte=number_of_guests).values_list('id', flat=True)


    print(categories)
    # json_data = json.dumps(categories)
    # return HttpResponse(json_data, content_type="application/json")
    return JsonResponse({"categories": list(categories)})

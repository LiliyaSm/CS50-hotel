from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Count
from django.http import HttpResponse
from .models import Booking, Room, RoomCategory, RoomImage, Transfer
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from django.views.generic.list import ListView
from django.views.generic import DetailView, View
from django import forms
from django.http import JsonResponse


now = str(datetime.date.today())
tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))

def deserialize(data):
    # converts json data to string
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
            'departure': forms.DateInput(attrs={'type': 'date', "value": tomorrow, "min": tomorrow}),
        }


class TransferForm(forms.ModelForm):

    class Meta:
        model = Transfer
        fields = ('arrivalDate', 'arrivalTime', 'flightNumber', "checked")

        help_texts = {
            "flightNumber": "Including letters and digits"
        }
        labels = {
            'flightNumber': "Flight number",
            'arrivalDate': "Arrival date",
            'arrivalTime': "Arrival time",
        }

        widgets = {
            'arrivalDate': forms.DateInput(attrs={'type': 'date', "value": now, "min": now}),
            "arrivalTime": forms.TimeInput(attrs={'type': 'time'}, format='%H:%M',),
            "checked": forms.CheckboxInput(),
        }        


def execute_query(queryOrder):

    # Dictionary params not supported with SQLite

    return Room.objects.raw('''select rooms.id
                from "reservations_room" as rooms
                where
                    rooms.category_id =  %s and
                    rooms.id not in(
                        select rooms.id
                        from "reservations_room" as rooms
                        left join "reservations_booking" as bookings on rooms.id=bookings.room_id
                        where rooms.category_id = %s and
                            (bookings.confirmed = 1 and
                            (((bookings.arrival < %s AND bookings.departure >= %s) OR
                            (bookings.arrival <= %s AND bookings.departure > %s) OR
                            (bookings.arrival >= %s AND bookings.departure <= %s))))
                        group by rooms.id)  ''',
                     [queryOrder["category"], queryOrder["category"], queryOrder["departure"], queryOrder["departure"],
                      queryOrder["arrival"], queryOrder["arrival"],
                      queryOrder['arrival'], queryOrder["departure"]
                      ])

class CategoryListView(ListView):
    """creates a list of all existing room categories"""
    queryset = RoomCategory.objects.all()
    template_name = 'reservations/rooms.html'


class CategoryDetail(DetailView):
    """creates a detailed view of chosen room category"""

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


class AboutView(View):
    """rendering items on the main page"""
    template_name = 'reservations/about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class BookingView(View):
    """renders room search page"""
    template_name = "reservations/booking.html"

    def get(self, request, *args, **kwargs):
        form = BookingForm(request.GET)
        available_rooms = RoomCategory.objects.all()

        if form.is_valid():
            # save user search in session in JSON format
            request.session['form_data'] = deserialize(form.cleaned_data)
        else:
            try:
                data = eval(request.session.get('form_data'))
                form = BookingForm(initial=data)
            except TypeError:
                #if form empty display all available rooms (first search)
                form = BookingForm()
                return render(request, self.template_name, {
                    "form": form, "available_rooms": available_rooms, 
            })       
        return render(request, self.template_name, {'form': form, "available_rooms": available_rooms})


    def post(self, request, *args, **kwargs):

        if BookingForm(request.POST).is_valid():
            try:
                # if previous order wasn't finished populate it with new data
                booking_entry = Booking.objects.get(
                        user=request.user, confirmed=False)
                form = BookingForm(
                    request.POST, instance=booking_entry)
            except Booking.DoesNotExist:
                form = BookingForm(request.POST)

            # get button value of data attr where category "id" is stored
            room_id = int(request.POST.get("room_id", ""))

            order = form.save(commit=False)
            order.user = request.user
            category = get_object_or_404(RoomCategory, pk=room_id)
            queryOrder = {'category': category.id,
                          'arrival': order.arrival, 'departure': order.departure}

            #   find available rooms for booking in chosen category
            rooms = execute_query(queryOrder)
            if rooms:
                room = rooms[0]
                order.room = room
                # calculate the price
                delta = form.cleaned_data["departure"] - form.cleaned_data["arrival"]
                total_price = getattr(category, "price")*delta.days
                order.calc_price = total_price

                order.save()
                return redirect("confirm")
            else:
                # all rooms from showed category are occupied
                return redirect("booking")



class ConfirmView(View):
    """renders order confirm page"""
    template_name = "reservations/confirm.html"
    transferForm = TransferForm()

    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, user=request.user, confirmed=False)
        return render(request, self.template_name, {"booking": booking, "transferForm": self.transferForm})

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(
            Booking, user=request.user, confirmed=False)
        transfer_confirm = TransferForm(request.POST)
        if transfer_confirm.is_valid() and transfer_confirm.cleaned_data["checked"]:
            transfer_confirm = transfer_confirm.save(commit=False)
            transfer_confirm.order = order
            transfer_confirm.save()

        # make sure that room is still available
        category = get_object_or_404(RoomCategory, pk=order.room.category.id) 

        queryOrder = {'category': category.id, 'arrival': order.arrival, 'departure': order.departure}
        query = execute_query(queryOrder)

        for r in query:
            print(r)

        # if chosen room is not available anymore, rewrite it with another room from the same category
        
        if query:
            if order.room.id != query[0].id:            
                order.room = query[0]
        else:
            # there is no free rooms
            return redirect("booking")

        order.confirmed = True
        order.save()
        return redirect("index")



def booking_submit(request):
    """ returns AJAX response with list of available categories' ids  """

    arrival = request.GET.get("arrival", "")
    departure = request.GET.get("departure", "")
    number_of_guests = int(request.GET.get("guests", ""))
    request.session['form_data'] = f"""{{\n 'arrival': '{arrival}',\n 'departure': '{departure}',
                                       'guests': {number_of_guests}\n}}"""

    # find available rooms
    queryOrder = {'category': number_of_guests,
                  'arrival': arrival, 'departure': departure}
    # Dictionary params not supported with SQLite
    rooms = Room.objects.raw('''select rooms.id 
                from "reservations_room" as rooms
                left join "reservations_roomcategory" as categories on rooms.category_id=categories.id
                where 
                    categories.capacity >= %s and 
                    rooms.id not in(
                        select rooms.id
                        from "reservations_room" as rooms 
                        left join "reservations_booking" as bookings on rooms.id=bookings.room_id
                        left join "reservations_roomcategory" as categories on rooms.category_id=categories.id
                        where categories.capacity >= %s and 
                            (bookings.confirmed = 1 and
                            (((bookings.arrival < %s AND bookings.departure >= %s) OR
                            (bookings.arrival <= %s AND bookings.departure > %s) OR
                            (bookings.arrival >= %s AND bookings.departure <= %s))))
                        group by rooms.id)  ''',
                             [queryOrder["category"], queryOrder["category"], 
                              queryOrder["departure"], queryOrder["departure"],
                              queryOrder["arrival"], queryOrder["arrival"],
                              queryOrder['arrival'], queryOrder["departure"]
                              ])

    categories = set(room.category.id for room in rooms)

    return JsonResponse({"categories": list(categories)})
                                                         

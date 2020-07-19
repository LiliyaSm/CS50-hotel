from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
# from django.db.models import Q
from django.http import HttpResponse
from .models import Booking, Room, RoomCategory, RoomImage
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from django.views.generic.list import ListView
from django.views.generic import DetailView, View
from django.contrib import messages
from django import forms


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
        def __init__(self,  *args,**kwargs):
            super(BookingForm, self).__init__(*args, **kwargs)
            self.fields['guests'].required = False

        # def clean_field(self):
        #     data = self.cleaned_data['guests']
        #     if not data:
        #         data = 1


class BookingExtentedForm(BookingForm):
    class Meta(BookingForm.Meta):
        fields = ('arrival', 'departure', "guests")
    # def __init__(self,request,*args,**kwargs):
    #     super(BookingExtentedForm, self).__init__(*args, **kwargs)
    #     self.fields['arrival'] = forms.CharField(
    #         label='Username', max_length=100, initial=request.session['some_var'])


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
    success_url = 'booking'
    form = BookingForm()
    def get(self, request, *args, **kwargs):
        # form =  ClockOutForm(instance=TimesheetEntry.objects.get(id=pk))
        return render(request, self.template_name, {'form': self.form})

    # request.session["arrival"] = form.cleaned_data["arrival"]
    # request.session["departure"] = form.cleaned_data["departure"]


    # arrival = request.GET.get('arrival')

    # form.save()


class BookingView(View):
    template_name = "reservations/booking.html"

    def get(self, request, *args, **kwargs):
        form = BookingForm(request.GET)
        if not form.is_valid():            
            try:
                data = eval(request.session.get('form_data'))
                form = BookingForm(initial=data)
            except TypeError:
                form = BookingForm()
            return render(request, self.template_name, {
                "form": form
            })
            form = BookingForm()
            return render(request, self.template_name, {'form': form})
        # save user search
        request.session['form_data'] = deserialize(form.cleaned_data)

        available_rooms = RoomCategory.objects.all()

        return render(request, self.template_name, {
            "form": form, "available_rooms": available_rooms
        })




    # arrival = request.GET['arrival']
    # arrival = request.GET.get('arrival')



# def index(request):
#     

#     if request.method == "GET":
#         return render(request, "reservations/index.html", {
#         })
#     

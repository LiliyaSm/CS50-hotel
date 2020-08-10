from django import forms
import datetime
from .models import Booking, Transfer

now = str(datetime.date.today())
tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('arrival', 'departure', "guests")
        widgets = {
            'arrival': forms.DateInput(attrs={'type': 'date', "value": now, "min": now}),
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

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
# from .models import Item, Cart, ItemOrder, ToppingsPrice
import json
import decimal
import datetime
import copy
from django.contrib import messages


def index(request):
    """rendering items on the main page"""

    # items = Item.objects.exclude(
    #     Q(group__dishType="Toppings") | Q(group__dishType="Extras"))
    return render(request, "reservations/index.html")

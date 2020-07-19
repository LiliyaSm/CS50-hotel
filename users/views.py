from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from users.forms import UserRegistrationForm
from .models import Profile
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# Create your views here.


def registration(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':

        # map the submitted form to the UserRegistrationForm
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # reloading the database after the signal, profile instance will load
            user.refresh_from_db()
            # set the cleaned data to the fields
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')

            form.save()
            # log in the user immediately with given name
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('booking')

        else:
            return render(request=request,
                          template_name="users/registration.html",
                          context={"form": form})

    # GET Request
    form = UserRegistrationForm()
    return render(request=request,
                  template_name="users/registration.html",
                  context={"form": form})


@login_required()
def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'users/user_profile.html', {"user": user})

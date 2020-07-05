from django.urls import path
# from . import views

from django.contrib import admin
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path("login/", auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True),
    #      name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    # path("registration", user_views.registration, name="registration"),
]
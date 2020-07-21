from django import forms
from django.contrib.auth.models import User 
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100, required=True)
    last_name = forms.CharField(
        max_length=100, required=True)
    email = forms.EmailField(
        max_length=100, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    citizenship = forms.CharField(required=False)
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', "email",
                  "citizenship", "phone_number")

    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well. 
        """
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile

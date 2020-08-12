from django import forms
from django.contrib.auth.models import User 
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
        }))
    first_name = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={
                                              'class': 'form-control',
                                              }))
    last_name = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={
                                                                     'class': 'form-control',
                                                                     }))
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={
            'class': 'form-control',
        }))
        
    password1=forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', "type":"password",
    }))

    password2=forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', "type": "password"
            }))                                                                                               

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    '''extended user profile'''
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    citizenship = forms.CharField(required=False)
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', "email",
                  "citizenship", "phone_number")

    def save(self, *args, **kwargs):
        """
        Update the primary email address and names on the related User object
        """
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile

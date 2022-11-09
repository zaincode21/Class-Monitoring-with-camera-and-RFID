from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'username','password1', 'password2']

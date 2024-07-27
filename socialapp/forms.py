from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile

class Registeruser(UserCreationForm):
    # first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Full name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}))
    
    class Meta:
        model=User
        fields=['email','username']



class Profileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'


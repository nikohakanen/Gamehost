from django.forms import ModelForm
from django.contrib.auth.models import User
from gamehost.models import SiteUser
from django import forms

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class SiteUserForm(ModelForm):
    class Meta:
        model = SiteUser
        exclude = ['user']

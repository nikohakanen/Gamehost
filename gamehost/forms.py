from django.forms import ModelForm, TextInput, Select
from django.contrib.auth.models import User
from gamehost.models import SiteUser, Game
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

class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ['developer']
        widgets = {
            'name': TextInput(),
            'category': Select()
        }
        labels = {
            'src': 'Game source URL',
            'thumbnail': 'Game thumbnail URL',
        }

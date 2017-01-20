from django.forms import ModelForm
from django.contrib.auth.models import User
from gamehost.models import SiteUser

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class SiteUserForm(ModelForm):
    class Meta:
        model = SiteUser
        exclude = ['user']

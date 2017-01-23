from django.shortcuts import render
from django.http import HttpResponse, Http404
from gamehost.models import Game, SiteUser
from gamehost.forms import UserForm, SiteUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

# Just to test how the views worked again.
def homeview(request):
    game_list = Game.objects.all()
    return render(request, 'home.html', {'games': game_list})


@login_required
def profile(request, user_id):
    try:
        profile = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    else:
        if int(request.user.id) is not int(user_id):
            return HttpResponse("Permission denied")
        else:
            return render(request, 'profile.html', {'profile': profile})



def register(request):
    # if this is a POST request we need to process the forms' data and register the user
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        siteuser_form = SiteUserForm(request.POST, prefix='siteuser')
        # check whether they are valid:
        if user_form.is_valid() and siteuser_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user.siteuser.developer_status = siteuser_form.cleaned_data['developer_status']
            user.save()
            return HttpResponse("Succesfully registered!")
    else:
        user_form = UserForm(prefix='user')
        siteuser_form = SiteUserForm(prefix='siteuser')

    return render(request, 'registration/register.html', {'user_form': user_form, 'siteuser_form': siteuser_form})

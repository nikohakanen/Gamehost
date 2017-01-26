from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from gamehost.models import Game, SiteUser
from gamehost.forms import UserForm, SiteUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.signing import TimestampSigner, SignatureExpired
from django.core import signing, mail

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

@login_required
def game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game not found!")
    else:
        has_purchased = request.user.siteuser.has_purchased_game(game)
        highscores = game.get_highscores(request.user.siteuser, False)
        return render(request, 'game.html', {'game': game,
                                             'has_purchased': has_purchased,
                                             'highscores': highscores})

def logout_view(request):
    logout(request)
    return render(request, 'message.html', {'message': 'Logged out.'})


def register(request):
    if request.user.is_authenticated():
        return redirect(homeview)
    # if this is a POST request we need to process the forms' data and register the user
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        siteuser_form = SiteUserForm(request.POST, prefix='siteuser')
        # check whether they are valid:
        if user_form.is_valid() and siteuser_form.is_valid():
            user = user_form.save(commit=False) #Create user, but don't save to the database yet
            user.is_active = False
            user.set_password(user.password)
            user.save()
            user.siteuser.developer_status = siteuser_form.cleaned_data['developer_status']
            user.save()
            user_form.save_m2m() #save the many-to-many data for the form

            # Send activation email
            signer = TimestampSigner()
            key = signer.sign(user.id)
            message = 'Visit the following link to activate your account: {}/activate/{}'.format(request.get_host(), key)
            with mail.get_connection() as connection:
                mail.EmailMessage(
                    'Your activation link', message, 'admin@gamesite.fi', [user.email], connection=connection, ).send()
            return render(request, 'message.html', {'message': 'An activation link was sent to your email adress!'})
    else:
        user_form = UserForm(prefix='user')
        siteuser_form = SiteUserForm(prefix='siteuser')

    return render(request, 'registration/register.html', {'user_form': user_form, 'siteuser_form': siteuser_form})

def activate(request, key):
    try:
        signer = TimestampSigner()
        user_id = signer.unsign(key, max_age=timedelta(days=2))
        user = User.objects.get(id=user_id)

        if user.is_active == False:
            user.is_active = True
            user.save()
            return render(request, 'message.html', {'message': 'Your account has been succesfully activated! Please login.'})
        else:
            return render(request, 'message.html', {'message': "The user has already been activated!"})

    except SignatureExpired:
        return render(request, 'message.html', {'message': "The activation link has been expired"})
    except signing.BadSignature:
        raise Http404("Invalid activation link")

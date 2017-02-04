from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from gamehost.models import Game, Highscore, Savedata, Transaction
from gamehost.forms import UserForm, SiteUserForm, GameForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.signing import TimestampSigner, SignatureExpired
from django.core import signing, mail
import json, datetime

# Create your views here.

# Just to test how the views worked again.
def homeview(request):
    game_list = Game.objects.all()
    return render(request, 'home.html', {'games': game_list})


@login_required(login_url='/login/')
def profile(request, user_id):
    try:
        profile = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    else:
        if int(request.user.id) is not int(user_id):
            return HttpResponse("Permission denied")
        else:
            if profile.siteuser.developer_status:
                #Get sales statistics for the developer
                games = Game.objects.filter(developer=profile.siteuser)
                #trans = []
                totals = {}
                datelist = {}
                now = datetime.datetime.today()
                today = datetime.date(now.year, now.month, now.day)
                i = 0
                for g in games:

                    transactions = Transaction.objects.filter(game=g)
                    totals.update({g.name: transactions.count()})
                    #trans.append(transactions)

                    dates = []
                    day_count = (today - g.publish_date).days + 1
                    for single_date in (g.publish_date + timedelta(n) for n in range(day_count)):
                        daily_data = []
                        daily_data.append(single_date)
                        dailytrans = transactions.filter(date=single_date).count()
                        daily_data.append(dailytrans)
                        dates.append(daily_data)
                    datelist.update({g.name: dates})

                print(totals)
                return render(request, 'profile.html', {'profile': profile, 'games': games, 'totalSalesList': totals, 'datelist': datelist})#, 'transactions': transactions})
            else:
                return render(request, 'profile.html', {'profile': profile})

@login_required(login_url='/login/')
def add_game(request):
    if request.user.siteuser.developer_status == False:
        return render(request, 'message.html', {'message': 'Please register as a developer if you want to add games.'})
    elif request.method == 'POST':
        game_form = GameForm(request.POST)

        if game_form.is_valid():
            newgame = game_form.save(commit=False)
            newgame.developer = request.user.siteuser
            newgame.save()
            game_form.save_m2m() #save the many-to-many data for the form
            return render(request, 'message.html', {'message': 'Your game was added!'})
    else:
        game_form = GameForm()

    return render(request, 'add_game.html', {'game_form': game_form })


@login_required(login_url='/login/')
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
                                             'highscores': highscores,
                                             'user': request.user})


def add_highscore(request):
    score = Highscore()
    game = Game.objects.get(name=request.GET.get('game'))
    score.game = game
    user = User.objects.get(username=request.GET.get('user'))
    score.player = user.siteuser
    score.score = request.GET.get('score')
    score.save()
    highscores = game.get_highscores(user.siteuser, False)
    return render(request, 'highscore.html', {'highscores': highscores})


def save_game(request):
    game = Game.objects.get(name=request.GET.get('game'))
    user = User.objects.get(username=request.GET.get('user'))
    data = request.GET.get('game_state')
    save = game.saveGame(user.siteuser, data)
    date = save.date.strftime("%B %d, %Y")
    return HttpResponse('Last saved ' + date)


def load_game(request):
    game = Game.objects.get(name=request.GET.get('game'))
    user = User.objects.get(username=request.GET.get('user'))
    msg = game.loadGame(user.siteuser)
    if msg is not "No data found":
        return JsonResponse({'messageType': 'LOAD', 'gameState': msg})
    else:
        return JsonResponse({'messageType': 'ERROR',
                            'info': 'Gamestate could not be loaded.'})


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

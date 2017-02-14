from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from gamehost.models import Game, Highscore, Savedata, Transaction, Payment
from gamehost.forms import UserForm, SiteUserForm, GameForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.signing import TimestampSigner, SignatureExpired
from django.core import signing, mail

import json, datetime
from hashlib import md5

PAYMENT_ID = "sid271828"
PAYMENT_KEY = "9846b7da3d25fc3b6ece0b753a47b099"

# Create your views here.

# Just to test how the views worked again.
def homeview(request):
    #game_list = Game.objects.all()
    return render(request, 'home.html', {})


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

                    transactions = Transaction.objects.filter(game=g, payment__status=Payment.SUCCESS)
                    totals.update({g.name: transactions.count()})
                    #trans.append(transactions)

                    dates = []
                    day_count = (today - g.publish_date).days + 1
                    for single_date in (g.publish_date + timedelta(n) for n in range(day_count)):
                        daily_data = []
                        daily_data.append(single_date)
                        dailytrans = transactions.filter(payment__date=single_date).count()
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

def games(request):
    genre = request.GET.get('genre')

    if genre == "all":
        games = Game.objects.all()
        return render(request, 'games.html', {'games': games})
    else:
        games = Game.objects.filter(category=genre)
        return render(request, 'games.html', {'games': games})

@login_required(login_url='/login/')
def edit_game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game not found!")
    else:
        if request.method == 'POST':
            game_form = GameForm(request.POST)

            if game_form.is_valid() and (int(request.user.id) is int(game.developer.user.id)):
                game = Game.objects.get(pk=game_id)
                game.name = game_form.cleaned_data['name']
                game.category = game_form.cleaned_data['category']
                game.price = game_form.cleaned_data['price']
                game.src = game_form.cleaned_data['src']
                game.thumbnail = game_form.cleaned_data['thumbnail']
                game.save()
                return render(request,
                              'message.html', {'message': 'Changes saved'})
            else:
                return HttpResponse('Something went wrong trying to edit')
        else:
            if int(request.user.id) is not int(game.developer.user.id):
                return HttpResponse("Permission denied.")
            else:
                data = {'name': game.name, 'category': game.category,
                        'price': game.price, 'src': game.src,
                        'thumbnail': game.thumbnail}
                form = GameForm(initial=data)
                return render(request,
                              'edit_game.html',
                              {'game_form': form, 'game': game})


@login_required(login_url='/login/')
def delete_game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game not found!")
    else:
        if request.method == "POST":
            if int(request.user.id) is int(game.developer.user.id):
                game.delete()
                return HttpResponse("Game deleted")
            else:
                return HttpResponse("Permission Denied")
        else:
            return render(request,
                          'delete_game.html',
                          {'object': game})

@login_required(login_url='/login/')
def purchased_games(request, user_id):
    try:
        user_profile = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    else:
        if int(request.user.id) is not int(user_id):
            return HttpResponse("Permission denied.")
        else:
            return render(
                            request,
                            'purchased_games.html',
                            {'user': user_profile})

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

def add_to_basket(request, game_id):
    if "basket" in request.session:
        request.session["basket"].add(game_id)
        request.session.modified = True
    else:
        request.session["basket"] = set(game_id)
    return render(request, "message.html", {"message": "Added {} to basket".format(game_id)})

def remove_from_basket(request, game_id):
    if "basket" in request.session:
        request.session["basket"].remove(game_id)
        request.session.modified = True
    contents = get_basket_contents(request)
    return render(request, "basket_contents.html", contents)

def empty_basket(request):
    """Empty the basket contents"""
    request.session["basket"] = set()
    request.session.modified = True

def get_basket_contents(request):
    games = []
    total = 0
    if "basket" in request.session:
        # Iterate a copy so removals work
        for game_id in request.session["basket"].copy():
            try:
                game = Game.objects.get(id=game_id);
                total += game.price;
                games.append(game)
            except:
                # Remove invalid item from basket
                request.session["basket"].remove(game_id)
                request.session.modified = True
    return {"games": games, "total": total, "modifiable": True}

def basket(request):
    contents = get_basket_contents(request)
    return render(request, "basket.html", contents)

@login_required(login_url='/login/')
def checkout(request):
    contents = get_basket_contents(request)
    payment = Payment.objects.create(total=contents["total"])
    for game in contents["games"]:
        Transaction.objects.create(player=request.user.siteuser, game=game, payment=payment, price=game.price)
    contents["modifiable"] = False
    contents["pid"] = payment.id
    contents["sid"] = PAYMENT_ID
    check_str = "pid={}&sid={}&amount={}&token={}".format(payment.id, PAYMENT_ID, contents["total"],
                                                          PAYMENT_KEY)
    m = md5(check_str.encode("ascii"))
    checksum = m.hexdigest()
    contents["checksum"] = checksum
    contents["host"] = "http://" + request.get_host()
    return render(request, "checkout.html", contents)

def payment_success(request):
    if "pid" in request.GET:
        try:
            payment = Payment.objects.get(id=request.GET["pid"])
            ref = request.GET["ref"]
            result = request.GET["result"]
            check_str = "pid={}&ref={}&result={}&token={}".format(payment.id, ref, result, PAYMENT_KEY)
            m = md5(check_str.encode("ascii"))
            checksum = m.hexdigest()
            if result == "success" and checksum == request.GET["checksum"]:
                payment.status = payment.SUCCESS
                payment.save()
                empty_basket(request)
                return render(request, "message.html", {"message": "Payment was succesfull"})
            else:
                payment.delete()
                return redirect(payment_error)
        except:
            return redirect(payment_lost)
    else:
        return redirect(payment_lost)

def payment_cancel(request):
    if "pid" in request.GET:
        try:
            Payment.objects.get(id=request.GET["pid"]).delete()
        except:
            pass
    return render(request, "message.html", {"message": "Payment was cancelled."})

def payment_error(request):
    if "pid" in request.GET:
        try:
            Payment.objects.get(id=request.GET["pid"]).delete()
        except:
            pass
    return render(request, "message.html", {"message": "Error with you payment."})

def payment_lost(request):
    return render(request, "message.html", {"message": "Sorry, we lost your payment."})

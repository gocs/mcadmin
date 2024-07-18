from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from asgiref.sync import sync_to_async

from .forms import SignupForm, LoginForm
from .models import Player, Payment
from .minecraft import execute_command, color_codes_replacer

import asyncio

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='general.log', level=logging.INFO)

# Create your views here.
# Home page
async def index(request):
    whitelist_list = ""
    try: whitelist_list = await execute_command('whitelist', 'list')
    except Exception as e: logger.critical("err whitelist_list: %s" % e)

    status = ""
    try: status = await execute_command('tps') # get server tick and memory usage
    except Exception as e: logger.critical("err status: %s" % e)

    current_user = await sync_to_async(lambda: request.user)()
    payments = []
    current_player = None
    if await sync_to_async(lambda: request.user.is_staff)():
        try: payments = [p async for p in Payment.objects.all()]
        except Exception as e: logger.critical("err payments: %s" % e)
    else:
        # get the player from the user
        try: player = await sync_to_async(lambda: Player.objects.get(id=current_user))()
        except Exception as e: logger.critical("err player: %s" % e)

        try: payments = [p async for p in Payment.objects.filter(player=player)]
        except Exception as e: logger.critical("err payments: %s" % e)

    # convert players in payments to sync
    z__payments = []
    for payment in payments:
        payment.z__player = await sync_to_async(lambda: payment.player)()
        z__payments.append(payment)

    players = []
    try: players = [p async for p in Player.objects.all()]
    except Exception as e: logger.critical("err players: %s" % e)

    # convert players into sync
    z__players = []
    for player in players:
        player.z__user = await sync_to_async(lambda: player.id)()
        z__players.append(player)

    player = {}
    payment = {}
    if request.method == 'GET':
        p = request.GET.get("player", "")
        if p != "":
            try: player = await sync_to_async(lambda: Player.objects.get(uuid=p))()
            except Exception as e: logger.warning("err getting player from request: %s" % e)

        p = request.GET.get("payment", "")
        if p != "":
            try: payment = await sync_to_async(lambda: Payment.objects.get(id=p))()
            except Exception as e: logger.warning("err getting payment from request: %s" % e)

    if player:
        player.z__user = await sync_to_async(lambda: player.id)()

    if payment:
        payment.z__player = await sync_to_async(lambda: payment.player)()

    # get all users to be a player
    users = [u async for u in get_user_model().objects.all()]

    return render(request, 'index.html', {
        'whitelist_list': color_codes_replacer(whitelist_list),
        'status': color_codes_replacer(status),
        'z__players': z__players,
        'z__payments': z__payments,
        'users': users,
        "player": player,
        "payment": payment,
        "current_user": current_user,
        "is_staff": await sync_to_async(lambda: request.user.is_staff)(),
        "is_authenticated": await sync_to_async(lambda: request.user.is_authenticated)(),
    })

# # signup page
# def user_signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try: user = authenticate(request, username=username, password=password)
            except: user = None
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

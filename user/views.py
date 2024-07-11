from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from rcon.source import rcon
from asgiref.sync import sync_to_async

from .forms import SignupForm, LoginForm, PlayerForm, PaymentForm
from .models import Player, Payment
from .minecraft import execute_command, color_codes_replacer

import httpx
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
    try: status = await execute_command('tps')
    except Exception as e: logger.critical("err status: %s" % e)

    players = []
    try: players = [p async for p in Player.objects.all()]
    except Exception as e: logger.critical("err players: %s" % e)

    payments = []
    try: payments = [p async for p in Payment.objects.all()]
    except Exception as e: logger.critical("err payments: %s" % e)

    # convert players in payments to sync
    z__payments = []
    for payment in payments:
        payment.z__player = await sync_to_async(lambda: payment.player)()
        z__payments.append(payment)

    return render(request, 'index.html', {
        'whitelist_list': color_codes_replacer(whitelist_list),
        'status': color_codes_replacer(status),
        'players': players,
        'z__payments': z__payments,
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

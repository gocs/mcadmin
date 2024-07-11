from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from django.conf import settings
from rcon.source import rcon
from rcon.source import Client
from asgiref.sync import sync_to_async

import httpx
import asyncio
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='general.log', level=logging.INFO)

host=settings.RCON_HOST
port=settings.RCON_PORT
passwd=settings.RCON_PASS

# Create your views here.
# Home page
async def index(request):
    logger.info("RCON_HOST: %s" % host)
    logger.info("RCON_PORT: %s" % port)
    logger.info("RCON_PASS: %s" % passwd)

    whitelist_list=''
    # with Client(host, port, passwd=passwd) as client:
    #     whitelist_list = client.run('whitelist', 'list')
    return render(request, 'index.html', {
        'whitelist_list': whitelist_list,
        "is_authenticated": await sync_to_async(lambda: request.user.is_authenticated)(),
    })

# # Home page async
# async def index(request):
#     logger.info("RCON_HOST: %s" % host)
#     logger.info("RCON_PORT: %s" % port)
#     logger.info("RCON_PASS: %s" % passwd)

#     response = await rcon('help', host=host, port=port, passwd=passwd)
#     print(response)
#     return render(request, 'index.html')

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
            user = authenticate(request, username=username, password=password)
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

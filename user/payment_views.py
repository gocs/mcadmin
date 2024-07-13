from django.shortcuts import render, redirect
from asgiref.sync import sync_to_async

from .models import Player, Payment
import asyncio

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='general.log', level=logging.INFO)

async def index(request):
    if not await sync_to_async(lambda: request.user.is_staff)():
        return redirect('home') # only staff can delete players
    if request.method != 'POST': return redirect('home') # only post requests

    if 'save' in request.POST:
        id = request.POST.get("save", "")
        if id != "":
            # get the player from the id
            p = None
            try: p = await sync_to_async(lambda: Payment.objects.get(id=id))()
            except Exception as e: logger.critical("err payment: %s" % e)
            if not p: return redirect('home')

            player = request.POST.get("player", "")
            if not player: return redirect('home') # name is required

            amount = request.POST.get("amount", "")
            if not amount: return redirect('home') # id is required

            p.player = await sync_to_async(lambda: Player.objects.get(uuid=player))()
            p.amount = amount
            await p.asave()

            return redirect('home')

        # create a new player
        logger.info("create a new player..")
        player = request.POST.get("player", "")
        if not player: return redirect('home') # name is required

        amount = request.POST.get("amount", "")
        if not amount: return redirect('home') # id is required

        # get the player from the id
        p = None
        try: p = await sync_to_async(lambda: Player.objects.get(uuid=player))()
        except Exception as e: logger.critical("err getting player: %s" % e)
        if not p: return redirect('home')

        payment = Payment(player=p, amount=amount)
        await payment.asave()
    elif 'delete' in request.POST:
        id = request.POST.get("delete", "")
        if not id: return redirect('home')

        # get the payment from the id
        p = None
        try: p = await sync_to_async(lambda: Payment.objects.get(id=id))()
        except Exception as e: logger.critical("err payment: %s" % e)
        if not p: return redirect('home')
        await p.adelete()

    return redirect('home')


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from .models import Player
from .minecraft import get_user

import asyncio

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='general.log', level=logging.INFO)

async def index(request):
    if not await sync_to_async(lambda: request.user.is_staff)():
        return redirect('home') # only staff can delete players
    if request.method != 'POST': return redirect('home') # only post requests

    if 'save' in request.POST:
        uuid = request.POST.get("save", "")

        # update the player
        if uuid != "":
            # get the player from the uuid
            p = None
            try: p = await sync_to_async(lambda: Player.objects.get(uuid=uuid))()
            except Exception as e: logger.critical("err getting player: %s" % e)
            if not p: return redirect('home')

            name = request.POST.get("name", "")
            if not name: return redirect('home') # name is required

            id = request.POST.get("id", "")
            if not id: return redirect('home') # id is required

            p.name = name
            p.id = await sync_to_async(lambda: get_user_model().objects.get(id=id))()
            await p.asave()

            return redirect('home')

        # create a new player
        name = request.POST.get("name", "")
        if not name: return redirect('home') # name is required

        id = request.POST.get("id", "")
        if not id: return redirect('home') # id is required

        # get the user from the id
        user = None
        try: user = await sync_to_async(lambda: get_user_model().objects.get(id=id))()
        except Exception as e: logger.critical("err user: %s" % e)
        if not user: return redirect('home')

        # get the minecraft user from the name
        mc_user = await get_user(name)
        if not mc_user: return redirect('home')

        p = Player(name=mc_user['name'], uuid=mc_user['id'], id=user)
        await p.asave()
    elif 'delete' in request.POST:
        uuid = request.POST.get("delete", "")
        if not uuid: return redirect('home') # uuid is required

        # get the player from the uuid
        p = None
        try: p = await sync_to_async(lambda: Player.objects.get(uuid=uuid))()
        except Exception as e: logger.critical("err deleting player: %s" % e)
        if not p: return redirect('home')
        await p.adelete()

    return redirect('home')

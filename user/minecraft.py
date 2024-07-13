from rcon.source import rcon
from asgiref.sync import sync_to_async
from django.conf import settings
from httpx import AsyncClient as ac

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='general.log', level=logging.INFO)

host=settings.RCON_HOST
port=settings.RCON_PORT
passwd=settings.RCON_PASS
api_url=settings.API_URL

# execute command in minecraft server using rcon
async def execute_command(*args):
    try: return await rcon(*args, host=host, port=port, passwd=passwd)
    except Exception as e: raise Exception("err execute_command: %s" % e)

# get minecraft user uuid by name in minecraft api
async def get_user(name):
    async with ac() as client:
        r = await client.get('%s/%s' % (api_url, name))
        return r.json()

    return None

# replace color codes in minecraft server
def color_codes_replacer(code):
    # Minecraft color codes
    # TODO: convert to propeer html color codes
    color_codes = {
        "§0": "",
        "§1": "",
        "§2": "",
        "§3": "",
        "§4": "",
        "§5": "",
        "§6": "",
        "§7": "",
        "§8": "",
        "§9": "",
        "§a": "",
        "§b": "",
        "§c": "",
        "§d": "",
        "§e": "",
        "§f": "",
        "§k": "",
        "§l": "",
        "§m": "",
        "§n": "",
        "§o": "",
        "§r": "",
    }
    for key, value in color_codes.items():
        code = code.replace(key, value)

    return code
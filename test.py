#from core import Core

from client import Client
from user import User
from core import Core

import asyncio

async def main():
    core = Core()
    response = await Client().authPassword(core, "mail@gmail.com", "password")
    response = await core.getAccessToken()
    response = await User().changePassword(core, response['access_token'], "hz", "hz")
    #response = await User().reactivateAccount(core, response['access_token'])
    print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
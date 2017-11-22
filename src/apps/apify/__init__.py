import uasyncio as asyncio

from uaos import App
from apps.network import Network
from .apify import HttpServer, Dispatcher, route


class Apify(App):
    requires = ['Network']
    not_mandatory = True

    async def __call__(self):
        await asyncio.start_server(HttpServer(Dispatcher()),
                                   host=Network.IP, port=8080)

Apify.register()

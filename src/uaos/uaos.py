import uasyncio as asyncio

try:
    from mocks import mock_apps
except ImportError as e:
    pass
import apps

from uaos.app import AppServer

class uaOS:
    @staticmethod
    def setup():
        AppServer.setup()

    @staticmethod
    def start():
        loop = asyncio.get_event_loop()
        AppServer.start(loop)
        loop.run_forever()
        loop.close()

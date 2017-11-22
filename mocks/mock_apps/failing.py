import uasyncio as asyncio
from uaos import App


class Setup(App):
    def __init__(self):
        super().__init__()
        raise RuntimeError()


class Run(App):
    async def __call__(self):
        await asyncio.sleep(2)
        raise RuntimeError()

Setup.register()
Run.register()

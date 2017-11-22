import gc
import uasyncio as asyncio
from uaos import App


class GC(App):
    async def __call__(self):
        while True:
            gc.collect()
            await asyncio.sleep(1)
GC.register()

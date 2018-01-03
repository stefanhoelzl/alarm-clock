from machine import WDT
import uasyncio as asyncio
from uaos import App


class Watchdog(App):
    def __init__(self):
        self.wdt = WDT(0)

    async def __call__(self):
        while True:
            self.wdt.feed()
            await asyncio.sleep(1)

Watchdog.register()

import uasyncio as asyncio

from apps import apify
from uaos import App


class Event:
    CMD = None

    def __init__(self, content):
        self.done = False
        self.cmd = content.strip()
        self.returns = None


class ExecEvent(Event):
    pass


class EvalEvent(Event):
    pass


class Repl(App):
    requires = ['Apify']

    events = []

    async def __call__(self):
        while True:
            await asyncio.sleep(0)
            if Repl.events:
                event = Repl.events.pop(0)
                try:
                    print("1")
                    if isinstance(event, ExecEvent):
                        event.returns = exec(event.cmd)
                    elif isinstance(event, EvalEvent):
                        event.returns = eval(event.cmd)
                except Exception as e:
                    event.returns = str(e)
                finally:
                    event.done = True

Repl.register()


async def do(event):
    Repl.events.append(event)
    while not event.done:
        await asyncio.sleep(0)
    return event.returns


@apify.route(b'/repl/exec')
async def execute(content):
    return await do(ExecEvent(content))


@apify.route(b'/repl/eval')
async def evaluate(content):
    return await do(EvalEvent(content))

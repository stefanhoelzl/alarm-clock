import uasyncio as asyncio

from apps import apify
from uaos import App


CMD = None
RET = None


class Repl(App):
    requires = ['Apify']

    events = []

    async def __call__(self):
        global CMD, RET
        while True:
            await asyncio.sleep(0.01)
            if CMD:
                if CMD[0] == "exec":
                    RET = exec(CMD[1])
                elif CMD[0] == "eval":
                    RET = eval(CMD[1])
                CMD = None

Repl.register()


async def do(f, content):
    global CMD
    CMD = f, content
    while CMD:
        await asyncio.sleep(0.01)
    return RET


@apify.route(b'/repl/exec')
async def execute(content):
    return await do("exec", content)


@apify.route(b'/repl/eval')
async def evaluate(content):
    return await do("eval", content)

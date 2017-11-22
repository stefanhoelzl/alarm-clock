import asyncio

from uaos import App


class AClient(App, asyncio.Protocol):
    async def __call__(self):
        loop = asyncio.get_event_loop()
        client = loop.create_connection(type(self), host='localhost', port=8080)
        await asyncio.sleep(0.1)
        await client

    def connection_made(self, transport):
        request = b"""POST /repl/exec HTTP/1.1\r
Content-Length: 3\r
\r
a=5\r
\r
"""
        print(request)
        transport.write(request)

    def data_received(self, data):
        print(data)


class BClient(App, asyncio.Protocol):
    async def __call__(self):
        loop = asyncio.get_event_loop()
        client = loop.create_connection(type(self), host='localhost',
                                        port=8080)
        await asyncio.sleep(1)
        await client

    def connection_made(self, transport):
        request = b"""POST /repl/eval HTTP/1.1\r
Content-Length: 3\r
\r
a\r
\r
"""
        print(request)
        transport.write(request)

    def data_received(self, data):
        print(data)

AClient.register()
BClient.register()

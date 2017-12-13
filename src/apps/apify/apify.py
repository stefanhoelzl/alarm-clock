import ujson

HTTP_STATUS_TEXT = {
    200: b"OK",
    400: b"Bad Request",
    405: b"Method Not Allowed",
    500: b"Internal Server Error"
}


def HttpStatusMixinCreator(http_states):
    name = "HttpStatusMixin"
    bases = ()
    dct = {}

    def get_fn(status_code):
        def fn(cls, content):
            return cls(status_code, content)

        return fn

    for code, text_whitespaces in http_states.items():
        status_text = text_whitespaces.decode('ascii').replace(" ", "")
        dct[status_text] = classmethod(get_fn(code))
    return type(name, bases, dct)


HttpStatusMixin = HttpStatusMixinCreator(HTTP_STATUS_TEXT)


class HttpError(Exception, HttpStatusMixin):
    def __init__(self, status_code, content):
        super().__init__()
        self.status_code = status_code
        self.content = content if content is not None else b""


class HttpResponse(HttpStatusMixin):
    VERSION = b"1.1"
    SERVER = b"micropython"

    def __init__(self, status_code, content):
        super().__init__()
        self.status_code = status_code
        self.content = content if content is not None else b""
        if not isinstance(self.content, bytes):
            self.content = bytes(self.content, "ascii")

    async def send(self, writer):
        header = b"HTTP/%s %d %s" % (self.VERSION,
                                     self.status_code,
                                     HTTP_STATUS_TEXT[self.status_code])
        content_length = b"Content-Length: %d" % len(self.content)
        response = b"\\r\\n".join((header,
                                   content_length,
                                   b'',
                                   self.content,
                                   b'',
                                   b''))
        await writer.awrite(response)


class HttpRequest:
    @classmethod
    async def from_reader(cls, reader):
        method, resource, version = (await reader.readline()).strip().split()
        parameter = {}
        content = None
        while True:
            try:
                key, value = (await reader.readline()).strip().split(b": ")
            except ValueError:
                break
            parameter[key] = value

        if b"Content-Length" in parameter:
            content = await reader.read(int(parameter[b'Content-Length']))

        return HttpRequest(method, resource, version, parameter, content)

    def __init__(self, method, resource, version, parameter, content):
        self.method = method
        self.resource = resource
        self.version = version
        self.parameter = parameter
        self.content = content


class HttpServer:
    ALLOWED_METHODS = (b'POST',)

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    async def dispatch(self, request):
        try:
            res = request.resource
            content = ujson.loads(request.content)
            ret = await self.dispatcher(res, content)
            if isinstance(ret, bytes):
                ret = ret.decode('ascii')
            response = HttpResponse.OK(ujson.dumps(ret))
        except Exception as e:
            response = HttpResponse.InternalServerError(repr(e))
        return response

    async def __call__(self, reader, writer):
        try:
            request = await HttpRequest.from_reader(reader)
            if request.method not in self.ALLOWED_METHODS:
                raise HttpError.MethodNotAllowed(request.method)
        except HttpError as e:
            response = HttpResponse(e.status_code,
                                    HTTP_STATUS_TEXT[e.status_code])
        else:
            response = await self.dispatch(request)
        await response.send(writer)


class Dispatcher:
    routes = {}

    @staticmethod
    def add_route(r, func):
        Dispatcher.routes[r] = func

    async def __call__(self, res, content):
        return await Dispatcher.routes[res](content)


def route(r):
    def decorator(func):
        Dispatcher.add_route(r, func)
        return func

    return decorator

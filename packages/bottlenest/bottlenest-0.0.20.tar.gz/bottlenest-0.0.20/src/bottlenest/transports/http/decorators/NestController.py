from bottlenest.core.NestProvider import NestProvider
from .NestRoute import NestRoute
from flask import request

# TODO: add support for route prefix


class NestController(NestProvider):
    __name__ = 'NestController'

    def __init__(self, providerClass, moduleContext):
        print(f"NestController init")
        self.moduleContext = moduleContext
        # TODO: I should pass moduleContext here (conditionally)
        self.providerClass = providerClass
        self.provider = providerClass()
        # moduleContext.getOrCreateProvider(self.__name__, self)
        # transport = moduleContext.getOrCreateTransport(self.transport)
        # instance = providerClass(moduleContext)
        # for route in self.routes:
        #     route = NestRoute(route)
        #     transport.addRoute(route)

    def _getMethodDecorators(self, provider):
        for key in dir(provider):
            if type(getattr(provider, key)).__name__ == 'NestRoute':
                yield getattr(provider, key)

    def listen(self, pool):
        print(f"NestController listen")
        flaskApp = self.moduleContext.getDefaultHttpTransport().getFlaskApp()
        for route in self._getMethodDecorators(self.provider):
            route.setupMethodDecorator(self.provider, NestRequest(flaskApp))
        # transport = self.moduleContext.getOrCreateTransport(self.transport)
        # transport.listen(pool, self.callback)


##################################################################


class NestRequest:
    __name__ = 'NestRequest'

    def __init__(self, flaskApp):
        self.flaskApp = flaskApp
        self.params = NestRequestParams(request)
        self.query = {}
        self.headers = {}

    @property
    def body(self):
        try:
            return request.json
        except RuntimeError:
            # occurs when we try to get body outside a request
            pass
        return {}


class NestRequestParams(object):
    __name__ = 'NestRequestParams'

    def __init__(self, request):
        super(NestRequestParams, self).__init__()
        self.request = request

    def __getattribute__(self, __name: str):
        if __name == 'request':
            return super(NestRequestParams, self).__getattribute__(__name)
        else:
            return self.request.view_args[__name]
            # return self.request.args.get(__name, type=str)

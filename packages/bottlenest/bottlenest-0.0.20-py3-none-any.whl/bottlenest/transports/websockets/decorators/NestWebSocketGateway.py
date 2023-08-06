import eventlet
import socketio
from bottlenest.core.NestProvider import NestProvider

servers = []


class NestWebSocketGateway(NestProvider):
    __name__ = 'NestWebSocketGateway'

    def __init__(self, gatewayClass, moduleContext, port=4001, namespace=None):
        self.port = port
        self.namespace = namespace
        self.providerClass = gatewayClass
        self.providerName = gatewayClass.__name__
        self.moduleContext = moduleContext
        # TODO: send moduleContext to gatewayClass(moduleContext)
        # conditionally
        try:
            self.provider = self.providerClass()
        except TypeError:
            self.provider = self.providerClass(moduleContext)

    def _getEvents(self, provider):
        for key in dir(provider):
            if type(getattr(provider, key)).__name__ == 'NestSubscribeMessage':
                yield getattr(provider, key)

    def listen(self, pool):
        print(f"NestSocketGateway listen {self.providerName}")

        def _startWebsocketsServer():
            print("starting websockets server")
            sio = socketio.Server()
            for event in self._getEvents(self.provider):
                event.setupMethodDecorator(self.provider, sio)
            app = socketio.WSGIApp(sio)
            eventlet.wsgi.server(eventlet.listen(('', self.port)), app)
        pool.spawn(_startWebsocketsServer)

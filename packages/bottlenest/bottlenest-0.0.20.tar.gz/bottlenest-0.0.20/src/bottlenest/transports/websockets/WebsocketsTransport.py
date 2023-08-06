from .factories.WebsocketsFactory import WebsocketsFactory
from bottlenest.core.NestTransport import NestTransport


class WebsocketsTransport(NestTransport):
    __sioids = 0

    # called by user, passing any options
    def __init__(self):
        pass

    def getTransportKey(self):
        WebsocketsTransport.__sioids += 1
        return 'WebsocketsTransport', f"sio-{WebsocketsTransport.__sioids}"

    def setupTransport(self, appContext, moduleContext):
        self.appContext = appContext
        self.moduleContext = moduleContext

    def listen(self, pool):
        pass

    # def listen(self, callback):
    #     # TODO: review this port to allow multiple ports
    #     port = self.appContext.get('port')
    #     app = self.appContext.get('app')
    #     eventlet.wsgi.server(eventlet.listen(('', port)), app)
    #     callback()

import eventlet
import socketio


class WebsocketsTransportClient:
    def __init__(self):
        pass

    def setupTransport(self, context):
        self.context = context
        self.module = self.context.get('module')
        self.logger = self.context.get('logger')
        sio = socketio.Server()
        app = socketio.WSGIApp(sio)
        context.set('sio', sio)
        context.set('app', app)

    def listen(self, callback):
        # TODO: review this port to allow multiple ports
        port = self.context.get('port')
        app = self.context.get('app')
        eventlet.wsgi.server(eventlet.listen(('', port)), app)
        callback()

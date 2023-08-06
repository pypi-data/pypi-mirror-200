from bottlenest.core.NestMethodDecorator import NestMethodDecorator


class NestSubscribeMessage(NestMethodDecorator):
    __name__ = 'NestSubscribeMessage'

    def __init__(self, callback, eventName):
        self.eventName = eventName
        self.callback = callback

    # called from whithin NestWebsocketGateway._setupProvider()
    def setupMethodDecorator(self, cls, sio):
        print(f"setup event {self.eventName}")

        @sio.on(self.eventName)
        def _callback(sid, data):
            print(f"NestSubscribeMessage {self.eventName}")
            result = self.callback(cls, data)
            if result is not None:
                sio.emit(self.eventName, result, room=sid)

import eventlet
import socketio
from ...http.HttpTransport import HttpTransport


class WebsocketsFactory:
    __gateways__: dict[str, dict] = {}
    __appContext__ = None

    @staticmethod
    def setAppContext(appContext) -> None:
        print("---x-x--x--x-------------x-x--x--------------> setAppContext")
        if WebsocketsFactory.__appContext__ is None:
            WebsocketsFactory.__appContext__ = appContext

    @staticmethod
    def registerGateway(provider, providerContext) -> None:
        # add gateway
        sio = socketio.Server()
        providerContext.set('sio', sio)
        WebsocketsFactory.__gateways__[provider.getName()] = {
            'provider': provider,
            'providerContext': providerContext,
            'sio': sio,
            # 'app': httpTransport.app,
            # 'port': provider.port,
        }

    @staticmethod
    def setupGateway(gatewayDict):
        sio = gatewayDict['sio']
        provider = gatewayDict['provider']
        providerContext = gatewayDict['providerContext']
        port = provider.port
        httpTransport = HttpTransport(port=provider.port)
        httpTransport.setupTransport(
            moduleContext=providerContext,
            appContext=WebsocketsFactory.__appContext__,
        )
        # app = socketio.WSGIApp(sio)

        def _onConnect(sid, environ, auth):
            print(f"[NestWebsocketsFactory] onConnect {sid}")
        sio.on('connect')(_onConnect)

        app = socketio.WSGIApp(sio, httpTransport.app)
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)
        print(f"[listen] Starting websockets server on port {port}")
        # pool.spawn(eventlet.wsgi.server,
        #           eventlet.listen(("", port)), app)
        # run pool.spawn with Flask (app) and eventlet.listen(("", port))
        # return pool.spawn(eventlet.wsgi.server,
        #                   eventlet.listen(("0.0.0.0", port)), app)

    @staticmethod
    def listen(pool) -> None:
        print("Listen WEBSOCKETSSSSSS now!")

        def startServer(gateways):
            for gateway in gateways:
                pool.spawn(WebsocketsFactory.setupGateway, gateway)

        return startServer(WebsocketsFactory.__gateways__.values())
        # asyncio.run(asyncio.
        # eventlet.wsgi.server(eventlet.listen(('', port)), app)

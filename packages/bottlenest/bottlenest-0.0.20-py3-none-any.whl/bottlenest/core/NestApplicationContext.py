import eventlet
from bottlenest.core.NestTransport import NestTransport
from bottlenest.transports.http.HttpTransport import HttpTransport


class NestApplicationContext:
    # {"TransportClass":{"transportId": NestTransport}}
    transports: dict = {}
    _defaultHttpTransport: HttpTransport | None = None

    def __init__(self, moduleClass, transport=None):
        if transport is None:
            transport = HttpTransport()
        self.addTransport(transport)
        self.module = moduleClass(self)

    def addTransport(self, transport) -> None:
        group, key = transport.getTransportKey()
        if group not in NestApplicationContext.transports:
            NestApplicationContext.transports[group] = {}
        NestApplicationContext.transports[group][key] = transport
        # add to _defaultHttpTransport if needed
        print(f"NestApplicationContext.addTransport {group} {key}")
        if NestApplicationContext._defaultHttpTransport is None and group == 'HttpTransport':
            NestApplicationContext._defaultHttpTransport = transport

    def getTransport(self, transport) -> NestTransport:
        group, key = transport.getTransportKey()
        if group not in NestApplicationContext.transports:
            raise Exception(
                f'Transport "{group}"."{key}" not found')
        if key not in NestApplicationContext.transports[group]:
            raise Exception(
                f'Transport "{group}"."{key}" not found')
        return NestApplicationContext.transports[group][key]

    def getDefaultHttpTransport(self) -> HttpTransport:
        if NestApplicationContext._defaultHttpTransport is None:
            raise Exception('Default HttpTransport not found')
        return NestApplicationContext._defaultHttpTransport

    def listen(self):
        # print(NestApplicationContext.transports)
        # setup the transports
        for group in NestApplicationContext.transports.values():
            for transport in group.values():
                transport.setupTransport(self, self.module.moduleContext)
        # create the pool
        # poolQtt = len(WebsocketsFactory.__gateways__.values()) + 1
        # pool = eventlet.GreenPool(poolQtt)
        pool = eventlet.GreenPool()
        # listen to transports
        for group in NestApplicationContext.transports.values():
            for transport in group.values():
                transport.listen(pool)
        # listen to module (and providers)
        self.module.listen(pool)
        # wait for all
        try:
            print("NestApplicationContext running...")
            pool.waitall()
        except KeyboardInterrupt:
            print("NestApplicationContext keyboard interrupt")
            # ? pool.kill()

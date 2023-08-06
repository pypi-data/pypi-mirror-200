import eventlet
from .HttpTransport import HttpTransport
from ..websockets.factories.WebsocketsFactory import WebsocketsFactory


class NestHttpModule(object):
    def __init__(self, moduleClass, imports, controllers, providers):
        self.isEnabled = False
        # module default options
        self.imports = imports
        self.controllers = controllers
        self.providers = providers
        # module variables
        self.moduleName = moduleClass.__name__
        self.moduleInstance = moduleClass()
        print(f"NestModule init", [self.moduleName])

    def enableModule(self):
        print(f"NestHttpModule enableModule {self.moduleName}")
        self.isEnabled = True
        for module in self.imports:
            print(f"enableModule", [module.moduleName])
            module.enableModule()
        for provider in self.providers:
            print(f"enableProvider", [provider.getName()])
            provider.enableProvider()

    # called automatically
    # when you run NestFactory.createMicroservice
    # (inside NestApplicationContext)
    def setupModule(self, appContext, moduleContext, transport=None):
        print(f"NestHttpModule setupModule {self.moduleName}")
        if not self.isEnabled:
            raise Exception(f"Module not enabled: {self.moduleName}")
        WebsocketsFactory.setAppContext(appContext)
        # Calls NestInputTransport.setupTransport()
        # creates the Flask app
        self.__setupInputTransport(
            transport=transport,
            appContext=appContext,
            moduleContext=moduleContext,
        )
        # run setup on any imported modules
        for module in self.imports:
            module.setupModule(appContext, moduleContext, transport)
        # run setup on providers
        # these are the most important ones
        for provider in self.providers:
            provider.setupProvider(self, moduleContext)
        # run setup on controllers
        # this is only used for HttpTransport
        for controller in self.controllers:
            controller.setupProvider(self, moduleContext)

    def __setupInputTransport(self, transport, appContext, moduleContext):
        if transport is None:
            transport = HttpTransport()
        self.transport = transport
        moduleContext.set('transport', transport)
        transport.setupTransport(
            appContext=appContext, moduleContext=moduleContext)
        return transport

    # proxy static methods
    def __getattr__(self, name):
        return getattr(self.moduleInstance, name)

    def listen(self):
        print(f"NestHttpModule listen {self.moduleName}")
        if not self.isEnabled:
            raise Exception(f"Module not enabled: {self.moduleName}")

        # print("------------------------ 1")
        # for module in self.imports:
        #     print("------------------------ 2 ", module.moduleName)
        #     if module.isEnabled:
        #         print("------------------------ 3")
        #         for provider in module.providers:
        #             print("------------------------ 4 ", provider.getName())
        #             if provider.isEnabled:
        #                 print("------------------------ 5")
        #                 provider.listen()
        #         # module.listen()

        poolQtt = len(WebsocketsFactory.__gateways__.values()) + 1
        pool = eventlet.GreenPool(poolQtt)
        # pool = eventlet.GreenPile()
        # runningServers = []

        def __listenTransport(self, pool):
            def callback():
                # self.logger.log(f"NestApplicationContext stopped")
                print(f"NestApplicationContext running callback")
            # self.transport = self.moduleContext.get('transport')
            if isinstance(self.transport, HttpTransport):
                # listen for websockets
                WebsocketsFactory.listen(pool)
                # runningServers.extend(gateways)
            # listen for http
            self.transport.listen(pool, callback)
        __listenTransport(self, pool)

        # for result in pool:
        #     print(f"NestApplicationContext result", result)
        try:
            print("NestApplicationContext running...")
            pool.waitall()
        except KeyboardInterrupt:
            print("NestApplicationContext keyboard interrupt")
            # for server in runningServers:
            #     server.kill()
        # ---
        # for server in runningServers:
        #     print(f"First server ended! {type(server)}")
        #     if isinstance(server, eventlet.greenthread.GreenThread):
        #         print("waiiit")
        #         server.wait()
        #         continue
        #     if server is not None:
        #         server.kill()
        # print("-----------------x------------------ ", runningServers)

        # while True:
        #     endAll = False
        #     for server in runningServers:
        #         # server is a GreenThread
        #         # check if it's pending
        #         if not server.dead:
        #             continue
        #         # check if it's dead
        #         else:
        #             endAll = True
        #             break
        #     if endAll:
        #         break
        #     eventlet.sleep(0.1)
        # print("NestApplicationContext ended")

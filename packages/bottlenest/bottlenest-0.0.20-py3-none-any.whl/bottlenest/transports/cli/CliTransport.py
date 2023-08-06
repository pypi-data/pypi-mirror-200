from bottlenest.core.NestTransport import NestTransport


class CliTransport(NestTransport):
    # called by user, passing any options
    def __init__(self):
        pass

    def getTransportKey(self):
        return 'CliTransport', f"app"

    def setupTransport(self, appContext, moduleContext):
        self.appContext = appContext
        self.moduleContext = moduleContext

    def listen(self, pool):
        pass

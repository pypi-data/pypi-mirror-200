# from bottlenest.core.NestTransport import NestTransport
from bottlenest.core.NestProvider import NestProvider
from pprint import pprint


class NestModuleContext:
    def __init__(self, appContext):
        self.appContext = appContext
        self.container = {}

    def get(self, key, defaultValue=None):
        # print("NestModuleContext get", key)
        return self.container[key] if key in self.container else defaultValue

    def set(self, key, value):
        # print("NestModuleContext set", key, value)
        self.container[key] = value

    def registerProvider(self, provider):
        # print("NestModuleContext registerProvider", provider.__name__)
        self.container[provider.__name__] = provider
        self._populateProvider(provider)

    def _populateProvider(self, provider):
        assert issubclass(type(
            provider), NestProvider), f"Provider {provider} must be a subclass of NestProvider"
        for annotation in provider.providerClass.__annotations__:
            # TODO: add providerInstance to ??
            providerInstance = provider.providerClass.__annotations__[
                annotation](self)
            setattr(provider.provider, annotation,
                    providerInstance.classInstance)

    def getOrCreateTransport(self, transport):
        try:
            transport = self.appContext.getTransport(transport)
        except Exception:
            self.appContext.addTransport(transport)
        return transport

    def getDefaultHttpTransport(self):
        return self.appContext.getDefaultHttpTransport()

from abc import ABC, abstractmethod, ABCMeta


# this is the context that is given to a function inside a controller
# or a subscribe message function
# it's not the class, but the method inside a class
class NestProviderContext(ABC):
    # nestProvider is an implementation of NestProvider
    #
    def __init__(self, nestProvider, moduleContext):
        self.provider = nestProvider
        self.moduleContext = moduleContext

    def get(self, key):
        if key.startswith('provider.'):
            return self.moduleContext.get(key.replace('provider.', ''))
        # getName = f"{self.provider.module.moduleName}.{key}"
        # return self.moduleContext.get(getName)
        return self.moduleContext.get(key)

    def inject(self, injectable):
        # getName = f"{self.provider.module.moduleName}.{injectable.providerName}"
        # provider = self.moduleContext.get(getName)
        provider = self.moduleContext.get(injectable.providerName)
        if provider is None:
            raise Exception(f"Provider not found: {injectable.providerName}")
        return provider.classInstance

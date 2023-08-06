from bottlenest.core.NestProvider import NestProvider


def Injectable():
    def wrapper(originalClass):
        def inner(moduleContext):
            return NestInjectable(
                originalClass=originalClass,
                moduleContext=moduleContext,
            )
        return inner
    return wrapper


class NestInjectable(NestProvider):
    __name__ = 'NestInjectable'

    def __init__(self, originalClass, moduleContext):
        self.providerName = originalClass.__name__
        self.originalClass = originalClass
        self.providerClass = originalClass
        # self.classInstance = None
        # TODO: moduleContext should be optional here
        self.classInstance = self.originalClass(moduleContext)
        self.provider = self.classInstance
        # self.dependencies = []

    def getName(self):
        return self.providerName

    def eventName(self):
        return self.providerName

    # def enableProvider(self):
    #    pass

    def setupInjectable(self, module, container):
        print(
            f"NestInjectable setupInjectable {self.providerName} {container}")
        # self.module = module
        # self.container = container
        # TODO: This should be a singleton manager
        self.classInstance = self.originalClass(container)
        # providerName = f"{module.moduleName}.{self.providerName}"
        providerName = self.providerName
        container.set(providerName, self)

    def __repr__(self):
        return f"{self.providerName}()"

    def __str__(self):
        return f"{self.providerName}()"

    def listen(self, pool):
        pass

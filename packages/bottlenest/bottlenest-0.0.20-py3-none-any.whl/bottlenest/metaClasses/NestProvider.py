from inspect import signature
from abc import ABC, abstractmethod, ABCMeta, abstractproperty
from bottlenest.metaClasses.NestProviderContext import NestProviderContext


class NestProvider(ABC):
    # def __call__(cls, *args, **kwargs):
    #    instance = super(NestProvider, cls).__call__(*args, **kwargs)
    #    # instance.setup(*args, **kwargs)
    #    return instance

    # @abstractmethod
    @property
    def name(self):
        return self.cls.__name__

    @property
    @abstractmethod
    def eventName(self):
        return 'NestEvent'

    def __init__(self, cls):
        self.cls = cls
        self.isEnabled = False
        # self.name = cls.__name__

    def enableProvider(self):
        self.isEnabled = True

    def _getEventNames(self):
        eventClassName = self.eventName()
        eventNames = dir(self.classInstance)
        eventNames = [name for name in eventNames if type(
            getattr(self.classInstance, name)).__name__ == eventClassName]
        return eventNames

    # overridable
    # called from whithin the module's setup
    def setupProvider(self, module, moduleContext):
        print("NestProvider setupProvider")
        self._setupProvider(module, moduleContext)

    def _setupProvider(self, module, moduleContext):
        print("NestProvider _setupProvider")
        # self.module = module
        # self.moduleContext = moduleContext
        # get number of arguments in __init__
        # if self.cls has a __init__ method with 2 args
        nargs = len(signature(self.cls.__init__).parameters)
        if nargs == 2:
            eventContext = NestProviderContext(self, moduleContext)
            self.classInstance = self.cls(eventContext)
        else:
            self.classInstance = self.cls()
        moduleContext.set(self.name, self)
        # self.classInstance = self.cls(moduleContext)
        eventNames = self._getEventNames()
        for eventName in eventNames:
            # print("---->> eventName: ", eventName)
            event = getattr(self.classInstance, eventName)
            event.setupMethodDecorator(self.classInstance, moduleContext)

    def listen(self, pool):
        pass

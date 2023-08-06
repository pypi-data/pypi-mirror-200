from bottlenest.core.NestModuleContext import NestModuleContext


class NestModule:
    def __init__(
        self,
        # from decorator
        moduleClass,
        imports,
        providers,
        controllers,
        # from NestApplicationContext
        appContext,
    ):
        self._modules = []
        self._providers = []
        # ? I'm not creating an instance of moduleClass here
        # ? should I?
        # moduleContext is exposed
        # because of NestApplicationContext.listen
        # TODO: Inject providers into moduleContext
        # each Provider should register itself in moduleContext
        # using e.g.:
        # moduleContext.registerProvider(self)
        self.moduleContext = NestModuleContext(appContext)
        for importedModule in imports:
            self._modules.append(importedModule(appContext))
        for provider in providers:
            providerInstance = provider(self.moduleContext)
            # TODO: is this assert correct?
            # assert str(type(providerInstance)).find('NestInjectable') > -1, \
            #     f"Provider {type(providerInstance)} is not NestInjectable"
            self._providers.append(providerInstance)
            self.moduleContext.registerProvider(providerInstance)
        for controller in controllers:
            providerInstance = controller(self.moduleContext)
            self._providers.append(providerInstance)
            self.moduleContext.registerProvider(providerInstance)

    def listen(self, pool):
        for module in self._modules:
            module.listen(pool)
        for provider in self._providers:
            provider.listen(pool)

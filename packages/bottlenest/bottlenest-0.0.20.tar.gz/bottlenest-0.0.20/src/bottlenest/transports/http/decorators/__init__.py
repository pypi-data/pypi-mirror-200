# from ..NestHttpModule import NestHttpModule
from bottlenest.core.NestModule import NestModule
from .NestController import NestController
from .NestRoute import NestRoute
from .NestBody import NestBody


def Module(controllers=[], providers=[], imports=[]):
    def wrapper(moduleClass):
        def inner(appContext):
            return NestModule(
                moduleClass=moduleClass,
                imports=imports,
                providers=providers,
                controllers=controllers,
                appContext=appContext,
            )
        return inner
    return wrapper


def Controller():
    def wrapper(controllerClass):
        def inner(moduleContext):
            return NestController(
                controllerClass,
                moduleContext,
            )
        return inner
    return wrapper


def Body(dto):
    def wrapper(callback):
        return NestBody(
            callback=callback,
            dto=dto,
        )
    return wrapper


def Get(path):
    def wrapper(func):
        return NestRoute(
            path=path,
            method='GET',
            callback=func,
        )
    return wrapper


def Post(path):
    def wrapper(func):
        return NestRoute(
            path=path,
            method='POST',
            callback=func,
        )
    return wrapper


def Put(path):
    def wrapper(func):
        return NestRoute(
            path=path,
            method='PUT',
            callback=func,
        )
    return wrapper


def Delete(path):
    def wrapper(func):
        return NestRoute(
            path=path,
            method='DELETE',
            callback=func,
        )
    return wrapper


def Patch(path):
    def wrapper(func):
        return NestRoute(
            path=path,
            method='PATCH',
            callback=func,
        )
    return wrapper

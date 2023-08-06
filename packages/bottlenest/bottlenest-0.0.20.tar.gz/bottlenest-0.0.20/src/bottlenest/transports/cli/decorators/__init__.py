from bottlenest.transports.cli.decorators.NestCommand import NestCommand
from bottlenest.transports.cli.decorators.NestCommandArgument import NestCommandArgument


def Command(name, *args, **kwargs):
    def wrapper(commandClass):
        def inner(moduleContext):
            return NestCommand(
                commandClass=commandClass,
                commandName=name,
                moduleContext=moduleContext,
                *args,
                **kwargs,
            )
        return inner
    return wrapper


def CommandArgument(name, optional=None, *args, **kwargs):
    def wrapper(callback):
        return NestCommandArgument(
            callback=callback,
            argumentName=name,
            optional=optional,
            *args,
            **kwargs,
        )
    return wrapper

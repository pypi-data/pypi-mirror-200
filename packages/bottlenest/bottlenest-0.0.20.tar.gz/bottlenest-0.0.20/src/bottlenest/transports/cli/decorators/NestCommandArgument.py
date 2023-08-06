class NestCommandArgument:
    __name__ = "NestCommandArgument"

    def __init__(
        self,
        argumentName,
        callback,
        optional,
        *args,
        **kwargs,
    ):
        self.argumentName = argumentName
        self.callback = callback
        self.optional = optional
        self.args = args
        self.kwargs = kwargs

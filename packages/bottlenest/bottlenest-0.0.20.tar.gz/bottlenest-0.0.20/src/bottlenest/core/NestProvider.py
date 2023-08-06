from abc import ABC


class NestProvider(ABC):
    __provider__ = True

    providerName: str
    providerClass: type
    provider: object

    def __init__(self, providerClass, moduleContext):
        print(f"NestProvider init")

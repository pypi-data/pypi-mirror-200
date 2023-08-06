from bottlenest.core.NestApplicationContext import NestApplicationContext
import os


class NestFactory:
    @staticmethod
    def create(moduleClass, transport=None):
        return NestApplicationContext(
            moduleClass=moduleClass,
            transport=transport,
        )

    @staticmethod
    def createMicroservice(moduleClass, transport=None):
        return NestApplicationContext(
            moduleClass=moduleClass,
            transport=transport,
        )

from bottlenest.common.Injectable import Injectable
from dotenv import load_dotenv
from bottlenest.common import Module
from bottlenest.config.ConfigService import ConfigService
import os


@Module(
    providers=[ConfigService],
)
class ConfigModule:
    pass


def forRoot(envFilePath='.env'):
    # load .env file and add to environment
    # to load a .env file we will use the dotenv package
    load_dotenv(envFilePath)
    return ConfigModule


ConfigModule.forRoot = staticmethod(forRoot)

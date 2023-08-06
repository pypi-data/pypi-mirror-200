from bottlenest.common import Module
from .AppService import AppService
from .AppController import AppController


@Module(
    imports=[],
    providers=[AppService],
    controllers=[AppController],
)
class AppModule:
    pass

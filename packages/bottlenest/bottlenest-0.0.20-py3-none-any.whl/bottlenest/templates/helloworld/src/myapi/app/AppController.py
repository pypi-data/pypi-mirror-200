from bottlenest.common import Controller, Get
from .AppService import AppService


@Controller()
class AppController:
    def __init__(self, context):
        self.appService = context.inject(AppService)

    @Get('/')
    def getHello(self, req):
        return self.appService.getHello()

    @Get('/hello/:name')
    def getHello2(self, req):
        return f"Hello {req.params.name}!"

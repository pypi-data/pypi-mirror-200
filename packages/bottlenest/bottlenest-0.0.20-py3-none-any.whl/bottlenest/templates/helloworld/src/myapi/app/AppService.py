from bottlenest.common import Injectable


@Injectable()
class AppService:
    def getHello(self):
        return "Hello World!"

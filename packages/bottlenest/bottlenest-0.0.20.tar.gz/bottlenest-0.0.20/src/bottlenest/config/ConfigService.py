from bottlenest.common import Injectable
import os


@Injectable()
class ConfigService:
    def __init__(self, context):
        pass

    def get(self, key):
        return os.environ[key]

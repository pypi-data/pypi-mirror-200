from flask import request
from functools import wraps
from bottlenest.core.NestMethodDecorator import NestMethodDecorator
import json


class NestRoute(NestMethodDecorator):
    __name__ = 'NestRoute'

    def __init__(self, path, method, callback):
        self.path = path
        self.method = method
        self.callback = callback

    def setupMethodDecorator(self, provider, request):
        print(f"[NestRoute] setupMethodDecorator {self.method} {self.path}")
        request.flaskApp.add_url_rule(
            self._nestjsToFlaskPath(self.path),
            methods=[self.method],
            view_func=self._callbackWrapper(provider, self.callback, request),
        )

    def _callbackWrapper(self, provider, callback, request):
        @wraps(callback)
        def wrapped(*args, **kwargs):
            def _asJson(resp):
                if hasattr(resp, '__fields__'):
                    return resp.json()
                return json.dumps(resp)
            if issubclass(type(callback), NestMethodDecorator):
                try:
                    return _asJson(callback.setupMethodDecorator(provider, request))
                except Exception as e:
                    raise e
            return _asJson(callback(provider, request))
            # return self.callback(context)
        return wrapped

    # Flask routing is different than NestJS routing
    def _nestjsToFlaskPath(self, path: str) -> str:
        result = ''
        parts = path.split('/')
        for part in parts:
            if part.startswith(':'):
                result += '/<' + part[1:] + '>'
            else:
                result += '/' + part
        return result[1:]

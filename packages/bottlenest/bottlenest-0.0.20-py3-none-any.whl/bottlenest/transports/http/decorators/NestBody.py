from bottlenest.core.NestMethodDecorator import NestMethodDecorator
from pydantic.error_wrappers import ValidationError
from bottlenest.transports.http.errors.BadRequestError import BadRequestError


class NestBody(NestMethodDecorator):
    __name__ = 'NestBody'

    def __init__(self, callback, dto):
        self.callback = callback
        self.dto = dto

    def setupMethodDecorator(self, moduleContext, request):
        # pydantic validates automatically
        self.dto(request.body)
        return self.callback(moduleContext, request)

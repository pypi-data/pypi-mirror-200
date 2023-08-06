from .HttpError import HttpError


class BadRequestError(HttpError):
    def __init__(self, messages=[]):
        super(BadRequestError, self).__init__(messages, 400)

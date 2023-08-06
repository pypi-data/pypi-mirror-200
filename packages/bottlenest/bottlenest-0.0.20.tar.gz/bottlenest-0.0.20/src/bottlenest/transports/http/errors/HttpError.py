class HttpError(Exception):
    def __init__(self, messages=[], statusCode=500):
        message = messages if isinstance(messages, str) else messages[0]
        super(HttpError, self).__init__(message)
        self.messages = messages
        self.statusCode = statusCode

    def toDict(self):
        # check if messages is a list
        if isinstance(self.messages, list):
            return {'messages': self.messages}
        return {'messages': [str(self.messages)]}

    def __str__(self):
        return self.messages

    def __repr__(self):
        return self.messages

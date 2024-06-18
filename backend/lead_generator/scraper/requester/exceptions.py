class QueryFailedException(Exception):
    def __init__(self, message="Query failed", meta={}):
        self.message = message
        self.meta = meta
        super().__init__(self.message)


class QueueOverflowException(Exception):
    def __init__(self, message="Stack is full", meta={}):
        self.message = message
        self.meta = meta
        super().__init__(self.message)

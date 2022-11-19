class ValidationException(Exception):
    def __init__(self, message, field):
        self.message = message
        self.field = field


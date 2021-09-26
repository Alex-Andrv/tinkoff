class InvalidMoveError(Exception):
    def __init__(self, message=""):
        super(InvalidMoveError, self).__init__(message)


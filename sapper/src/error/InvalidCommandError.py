class InvalidCommandError(Exception):
    def __init__(self, message=""):
        super(InvalidCommandError, self).__init__(message)


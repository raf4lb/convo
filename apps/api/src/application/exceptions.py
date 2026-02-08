class InvalidUserError(Exception):
    def __init__(self, errors: list[str]):
        self.errors = errors


class ReceiverContactDoesNotExistError(Exception):
    pass

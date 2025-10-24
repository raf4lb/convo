import uuid

from src.domain.enums import UserTypes


class User:
    def __init__(self, id: uuid.UUID, name: str, email: str, type: UserTypes):
        self.id = id
        self.name = name
        self.email = email
        self.type = type

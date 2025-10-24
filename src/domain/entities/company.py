import uuid


class Company:
    def __init__(self, id: uuid.UUID, name: str):
        self.id = id
        self.name = name

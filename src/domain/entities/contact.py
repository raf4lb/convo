import uuid


class Contact:
    def __init__(self, id: uuid.UUID, name: str, phone_number: str):
        self.id = id
        self.name = name
        self.phone_number = phone_number

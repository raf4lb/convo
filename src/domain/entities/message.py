import uuid


class Message:
    def __init__(
        self,
        id: uuid.UUID,
        company_id: uuid.UUID,
        contact_id: uuid.UUID,
        text: str,
        timestamp: str,
    ):
        self.id = id
        self.company_id = company_id
        self.contact_id = contact_id
        self.text = text
        self.timestamp = timestamp

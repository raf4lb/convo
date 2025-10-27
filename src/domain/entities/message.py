class Message:
    def __init__(
        self,
        id: str,
        company_id: str,
        sender_id: str,
        receiver_id: str,
        received: bool,
        text: str,
        created_at: str,
        updated_at: str,
    ):
        self.id = id
        self.company_id = company_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.received = received
        self.text = text
        self.created_at = created_at
        self.updated_at = updated_at
